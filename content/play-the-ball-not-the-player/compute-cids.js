/**
 * Pure Node.js IPFS CID Computation (no external deps)
 * Computes CIDv1 with raw codec + sha2-256 for single files.
 * Encoded as base32 (lowercase, no padding) per IPFS CIDv1 spec.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// --- Base32 Encoding (RFC 4648 lowercase, no padding) ---
const BASE32_ALPHABET = 'abcdefghijklmnopqrstuvwxyz234567';

function base32Encode(bytes) {
  let bits = 0;
  let value = 0;
  let output = '';
  for (let i = 0; i < bytes.length; i++) {
    value = (value << 8) | bytes[i];
    bits += 8;
    while (bits >= 5) {
      output += BASE32_ALPHABET[(value >>> (bits - 5)) & 31];
      bits -= 5;
    }
  }
  if (bits > 0) output += BASE32_ALPHABET[(value << (5 - bits)) & 31];
  return output;
}

function base32Decode(str) {
  const bytes = [];
  let bits = 0, value = 0;
  for (let i = 0; i < str.length; i++) {
    const idx = BASE32_ALPHABET.indexOf(str[i].toLowerCase());
    if (idx === -1) continue;
    value = (value << 5) | idx;
    bits += 5;
    if (bits >= 8) { bytes.push((value >>> (bits - 8)) & 0xff); bits -= 8; }
  }
  return Buffer.from(bytes);
}

function multihashSHA256(data) {
  const hash = crypto.createHash('sha256').update(data).digest();
  return Buffer.concat([Buffer.from([0x12, 0x20]), hash]);
}

function computeCIDv1Raw(data) {
  const mh = multihashSHA256(data);
  const cidBytes = Buffer.concat([Buffer.from([0x01, 0x55]), mh]);
  return 'b' + base32Encode(cidBytes);
}

function encodeVarint(num) {
  const bytes = [];
  while (num > 0x7f) { bytes.push((num & 0x7f) | 0x80); num >>>= 7; }
  bytes.push(num & 0x7f);
  return Buffer.from(bytes);
}

function encodeDAGPBLink(name, cidStr, size) {
  const cidBytes = base32Decode(cidStr.slice(1));
  const nameBytes = Buffer.from(name, 'utf8');
  const nameField = Buffer.concat([Buffer.from([0x0a]), encodeVarint(nameBytes.length), nameBytes]);
  const tsizeField = Buffer.concat([Buffer.from([0x18]), encodeVarint(size)]);
  const hashField = Buffer.concat([Buffer.from([0x22]), encodeVarint(cidBytes.length), cidBytes]);
  return Buffer.concat([nameField, tsizeField, hashField]);
}

function encodeDAGPBNode(links) {
  const sorted = [...links].sort((a, b) => a.name.localeCompare(b.name));
  const linkFields = [];
  for (const link of sorted) {
    const lb = encodeDAGPBLink(link.name, link.cid, link.size);
    linkFields.push(Buffer.concat([Buffer.from([0x12]), encodeVarint(lb.length), lb]));
  }
  return Buffer.concat([Buffer.from([0x0a, 0x00]), ...linkFields]);
}

function computeDirCID(links) {
  const dagBytes = encodeDAGPBNode(links);
  const mh = multihashSHA256(dagBytes);
  const cidBytes = Buffer.concat([Buffer.from([0x01, 0x70]), mh]);
  return 'b' + base32Encode(cidBytes);
}

// --- Main ---
const CONTENT_DIR = __dirname;
const FILES = ['README.md', 'blog-post.md', 'content-series.md', 'slide-deck.md', 'philosophical-essay.md'];

console.log('=== IPFS CID Computation (Pure Node.js) ===\n');

const fileResults = [];
for (const file of FILES) {
  const filePath = path.join(CONTENT_DIR, file);
  if (!fs.existsSync(filePath)) { console.log(`  [SKIP] ${file}`); continue; }
  const content = fs.readFileSync(filePath);
  const cid = computeCIDv1Raw(content);
  const sha256hex = crypto.createHash('sha256').update(content).digest('hex');
  fileResults.push({ file, size: content.length, cid, sha256hex });
  console.log(`  [OK] ${file}  CID=${cid}  (${content.length.toLocaleString()}B)`);
}

console.log('\nComputing root directory CID...');
const rootCID = computeDirCID(fileResults.map(f => ({ name: f.file, cid: f.cid, size: f.size })));
console.log(`  Root CID: ${rootCID}\n`);

const manifest = {
  name: 'play-the-ball-not-the-player',
  description: 'A life lesson from the 2026 FIFA World Cup: play the ball, not the player.',
  generated: new Date().toISOString(),
  rootCID,
  files: fileResults.map(f => ({ path: f.file, cid: f.cid, size: f.size })),
  gatewayUrls: [
    `https://ipfs.io/ipfs/${rootCID}`,
    `https://cloudflare-ipfs.com/ipfs/${rootCID}`,
    `https://dweb.link/ipfs/${rootCID}`,
  ]
};

console.log('=== IPFS Pin Manifest ===\n');
console.log(JSON.stringify(manifest, null, 2));

fs.writeFileSync(path.join(CONTENT_DIR, 'ipfs-manifest.json'), JSON.stringify(manifest, null, 2));
console.log('\n[SAVED] ipfs-manifest.json');

const cidList = [
  `# IPFS CIDs — Play the Ball, Not the Player`,
  `# Generated: ${new Date().toISOString()}`,
  `${rootCID}`,
  ...fileResults.map(f => `${f.cid}  ${f.file}`),
  ``,
  `https://ipfs.io/ipfs/${rootCID}`,
  `https://cloudflare-ipfs.com/ipfs/${rootCID}`,
  `https://dweb.link/ipfs/${rootCID}`,
].join('\n');
fs.writeFileSync(path.join(CONTENT_DIR, 'IPFS_CIDS.txt'), cidList);
console.log('[SAVED] IPFS_CIDS.txt\n=== DONE ===');
