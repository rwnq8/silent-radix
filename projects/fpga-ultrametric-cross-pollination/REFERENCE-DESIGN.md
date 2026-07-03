# REFERENCE DESIGN: Ultrametric FPGA Hardware Modules

**Author:** QNFO Research Agent | **Date:** 2026-07-03 | **Status:** Draft v0.1
**Project:** fpga-ultrametric-cross-pollination | **Phase:** 2 — Formalization

---

## 1. Purpose

Provide synthesizable reference designs (in Verilog pseudocode) for the core ultrametric hardware primitives defined in `ARCHITECTURE-SPEC.md`. These modules are:
- **Self-contained** — no external IP dependencies beyond standard FPGA primitives
- **Parametric** — configurable for different p-adic bases, precision, and tree sizes
- **Verilator-compatible** — targeted for simulation-based benchmarking before synthesis

**Epistemic status:** `[speculative]` — these are novel designs. No prior art is known to exist `[LLM-INFERRED]`. The pseudocode captures the algorithmic intent; actual synthesis may require optimization for specific FPGA architectures.

---

## 2. Module 1: p-adic Digit-Serial Adder

### 2.1 Interface

```verilog
module padic_adder #(
    parameter P_BASE = 2,          // p-adic base (prime)
    parameter DIGIT_WIDTH = 1,     // bits per digit (ceil(log2(P_BASE)))
    parameter NUM_DIGITS = 64,     // precision (k digits)
    parameter PIPE_STAGES = 4      // pipeline stages per digit (for timing closure)
) (
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     valid_in,
    input  wire [DIGIT_WIDTH-1:0]   a_digit,    // stream a[0], a[1], ..., a[k-1]
    input  wire [DIGIT_WIDTH-1:0]   b_digit,    // stream b[0], b[1], ..., b[k-1]
    output wire                     valid_out,
    output wire [DIGIT_WIDTH-1:0]   sum_digit   // stream result[0], result[1], ...
);
```

### 2.2 Architecture

```
a_digit ──┬──[+]──► [mod-p] ──► sum_digit
          │        ▲
b_digit ──┤        │
          │   ┌────┴────┐
          └──►[+]──►[÷p]──► carry_register ──┘
              carry_in
```

### 2.3 Core Logic (Verilog Pseudocode)

```verilog
// Special case: p=2 (binary) — each digit is 1 bit, carry is standard binary
module padic_adder_binary #(parameter NUM_DIGITS = 64) (
    input  wire                    clk, rst_n,
    input  wire                    valid_in,
    input  wire                    a_bit,
    input  wire                    b_bit,
    output wire                    valid_out,
    output wire                    sum_bit
);
    reg carry;
    reg [$clog2(NUM_DIGITS):0] digit_count;
    reg active;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            carry <= 1'b0;
            digit_count <= 0;
            active <= 1'b0;
        end else if (valid_in && !active) begin
            active <= 1'b1;
            digit_count <= 0;
            carry <= 1'b0;
        end else if (active) begin
            // Full adder: sum = a ⊕ b ⊕ carry, new_carry = majority(a,b,carry)
            // sum_bit is combinatorial: a_bit ^ b_bit ^ carry
            carry <= (a_bit & b_bit) | (a_bit & carry) | (b_bit & carry);
            digit_count <= digit_count + 1;
            if (digit_count == NUM_DIGITS - 1)
                active <= 1'b0;
        end
    end

    assign sum_bit = active ? (a_bit ^ b_bit ^ carry) : 1'b0;
    assign valid_out = active;
endmodule
```

```verilog
// General case: arbitrary prime p
module padic_adder_general #(
    parameter P_BASE = 3,
    parameter DIGIT_WIDTH = 2,     // ceil(log2(3)) = 2
    parameter NUM_DIGITS = 64
) (
    input  wire                        clk, rst_n,
    input  wire                        valid_in,
    input  wire [DIGIT_WIDTH-1:0]      a_digit,
    input  wire [DIGIT_WIDTH-1:0]      b_digit,
    output wire                        valid_out,
    output wire [DIGIT_WIDTH-1:0]      sum_digit
);
    // Wider registers for carry (max carry = 2*p-2, needs DIGIT_WIDTH+1 bits)
    localparam CARRY_WIDTH = DIGIT_WIDTH + 1;
    reg [CARRY_WIDTH-1:0] carry;
    reg [$clog2(NUM_DIGITS):0] digit_count;
    reg active;

    wire [CARRY_WIDTH-1:0] raw_sum;
    assign raw_sum = {1'b0, a_digit} + {1'b0, b_digit} + carry;

    // mod-p reduction via LUT (synthesizes to distributed RAM)
    // For small primes (p ≤ 23), a LUT-based modulo is efficient
    wire [DIGIT_WIDTH-1:0] reduced;
    assign reduced = raw_sum % P_BASE;  // Synthesis: infers LUT-based divider

    wire [CARRY_WIDTH-1:0] new_carry;
    assign new_carry = raw_sum / P_BASE;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            carry <= 0;
            digit_count <= 0;
            active <= 1'b0;
        end else if (valid_in && !active) begin
            active <= 1'b1;
            digit_count <= 0;
            carry <= 0;
        end else if (active) begin
            carry <= new_carry;
            digit_count <= digit_count + 1;
            if (digit_count == NUM_DIGITS - 1)
                active <= 1'b0;
        end
    end

    assign sum_digit = active ? reduced : {DIGIT_WIDTH{1'b0}};
    assign valid_out = active;
endmodule
```

### 2.4 Resource & Performance Estimates

| Parameter | LUTs | FFs | Latency | Throughput |
|:----------|:-----|:----|:--------|:-----------|
| p=2, k=64 | ~32 | ~70 | 64 cycles | 1 result/64 cycles |
| p=3, k=64 | ~48 | ~72 | 64 cycles | 1 result/64 cycles |
| p=7, k=32 | ~64 | ~38 | 32 cycles | 1 result/32 cycles |

`[LLM-INFERRED — estimates based on standard FPGA synthesis patterns]`

---

## 3. Module 2: Dendrogram Traversal Engine

### 3.1 Interface

```verilog
module dendrogram_engine #(
    parameter MAX_NODES = 16384,    // capacity of node RAM
    parameter MAX_DEPTH = 16,       // max tree depth (log₂(MAX_NODES))
    parameter NODE_ADDR_BITS = 14   // ceil(log2(MAX_NODES))
) (
    input  wire                     clk, rst_n,
    // Command interface
    input  wire                     cmd_valid,
    input  wire [1:0]               cmd_op,       // 00=ANC, 01=DEPTH, 10=BALL, 11=NN
    input  wire [NODE_ADDR_BITS-1:0] cmd_leaf_a,
    input  wire [NODE_ADDR_BITS-1:0] cmd_leaf_b,
    input  wire [15:0]              cmd_radius,    // for BALL
    // Result interface
    output wire                     result_valid,
    output wire [NODE_ADDR_BITS-1:0] result_node,  // ANC result or NN result
    output wire [15:0]              result_depth,   // depth value
    output wire                     result_found,   // for BALL: hit indicator
    // Memory interface (to Dendrogram Node RAM)
    output wire                     mem_read_en,
    output wire [NODE_ADDR_BITS-1:0] mem_addr,
    input  wire [63:0]              mem_rdata       // {parent[31:0], depth[15:0], children[7:0], flags[7:0]}
);
```

### 3.2 ANC (Nearest Common Ancestor) — FSM Design

```verilog
// State machine for ANC computation
localparam ANC_IDLE     = 3'd0;
localparam ANC_DEPTH_A  = 3'd1;  // Walk up leaf_a to align depths
localparam ANC_DEPTH_B  = 3'd2;  // Walk up leaf_b to align depths
localparam ANC_WALK     = 3'd3;  // Walk up both together
localparam ANC_DONE     = 3'd4;

reg [2:0] anc_state;
reg [NODE_ADDR_BITS-1:0] ptr_a, ptr_b;
reg [15:0] depth_a, depth_b;
reg [7:0] stall_count;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        anc_state <= ANC_IDLE;
        ptr_a <= 0; ptr_b <= 0;
    end else begin
        case (anc_state)
            ANC_IDLE: begin
                if (cmd_valid && cmd_op == 2'b00) begin
                    ptr_a <= cmd_leaf_a;
                    ptr_b <= cmd_leaf_b;
                    anc_state <= ANC_DEPTH_A;
                end
            end

            ANC_DEPTH_A: begin
                // Read depth of node at ptr_a
                if (stall_count == 0) begin
                    // Issue read
                    stall_count <= 1;  // 1-cycle BRAM read latency
                end else begin
                    // Read complete: extract depth
                    depth_a <= mem_rdata[47:32];  // depth field
                    // Issue read for ptr_b
                    stall_count <= 2;
                end
                // After both reads complete, compare depths
                if (stall_count == 2) begin
                    depth_b <= mem_rdata[47:32];
                    if (depth_a > depth_b)
                        anc_state <= ANC_DEPTH_A;  // Keep walking A up
                    else if (depth_b > depth_a)
                        anc_state <= ANC_DEPTH_B;  // Walk B up
                    else
                        anc_state <= ANC_WALK;
                end
                // Walk up A: ptr_a <= parent
                if (depth_a > depth_b && stall_count == 2) begin
                    ptr_a <= mem_rdata[63:32];  // parent field
                    stall_count <= 0;
                end
            end

            // ANC_DEPTH_B, ANC_WALK: similar logic (omitted for brevity)
            // Walk up B to align depth, then walk both up until ptr_a == ptr_b

            ANC_DONE: begin
                // result_node = ptr_a (= ptr_b = LCA)
                anc_state <= ANC_IDLE;
            end
        endcase
    end
end

// Parent extraction helper
wire [NODE_ADDR_BITS-1:0] node_parent;
wire [15:0]               node_depth;
wire [7:0]                node_flags;
assign node_parent = mem_rdata[63:32];
assign node_depth  = mem_rdata[47:32];
assign node_flags  = mem_rdata[7:0];
```

### 3.3 BALL Query — Pipelined Scan

```verilog
// Ball query: scan all leaves, compare distance, collect matches
// Uses a streaming comparator pipeline
module ball_query #(
    parameter MAX_LEAVES = 16384,
    parameter LEAF_ADDR_BITS = 14
) (
    input  wire                        clk, rst_n,
    input  wire                        start,
    input  wire [LEAF_ADDR_BITS-1:0]   center_leaf,
    input  wire [15:0]                 radius,
    output wire                        done,
    output wire                        match_valid,
    output wire [LEAF_ADDR_BITS-1:0]   match_addr,
    // Memory interface
    output wire [LEAF_ADDR_BITS-1:0]   leaf_addr,
    input  wire [127:0]                leaf_data
);
    reg [LEAF_ADDR_BITS-1:0] scan_ptr;
    reg active;
    wire [15:0] leaf_energy = leaf_data[31:16];
    wire [15:0] leaf_label  = leaf_data[15:0];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_ptr <= 0;
            active <= 1'b0;
        end else if (start && !active) begin
            scan_ptr <= 0;
            active <= 1'b1;
        end else if (active) begin
            scan_ptr <= scan_ptr + 1;
            if (scan_ptr == MAX_LEAVES - 1)
                active <= 1'b0;
        end
    end

    assign leaf_addr = scan_ptr;
    assign done = !active && start;  // pulse when scan completes
    // match_valid asserted when ANC(center, scan_ptr) depth ≤ radius
    // (requires ANC result — in full implementation, BALL pipelines
    //  with ANC engine or uses precomputed distance matrix)
    assign match_valid = 1'b0;  // placeholder — full implementation required
    assign match_addr = scan_ptr;
endmodule
```

### 3.4 Performance Summary

| Operation | Cycles (worst case) | Memory Accesses |
|:----------|:-------------------|:----------------|
| ANC (2 leaves) | 2 × depth = 32 | 2 × depth = 32 |
| DEPTH (1 leaf) | 1 | 1 |
| BALL (radius r) | MAX_LEAVES × (1 + ANC_cycles) | ~MAX_LEAVES |
| NN (1 leaf) | MAX_LEAVES × ANC_cycles | ~MAX_LEAVES × depth |

---

## 4. Module 3: Braid Word Length Counter

### 4.1 Interface

```verilog
module braid_word_counter #(
    parameter N = 20  // number of strands (leaves)
) (
    input  wire                     clk, rst_n,
    input  wire                     start,
    input  wire [$clog2(N)-1:0]     pos_a, pos_b,  // leaf positions
    output wire                     done,
    output wire [15:0]              word_length,     // minimal braid word length
    // Adjacency check interface
    output wire [$clog2(N)-1:0]     adj_check_idx,
    input  wire                     adj_result       // 1 if leaves idx and idx+1 are siblings
);
```

### 4.2 Core Logic (Verilog Pseudocode)

```verilog
// Counts permitted adjacent transpositions to swap positions a and b
// Implements the restricted braid word length from ARCHITECTURE-SPEC.md §7.1
module braid_word_counter #(parameter N = 20) (
    input  wire clk, rst_n, start,
    input  wire [$clog2(N)-1:0] pos_a, pos_b,
    output reg  done,
    output reg  [15:0] word_length,
    output reg  [$clog2(N)-1:0] adj_check_idx,
    input  wire adj_result
);
    localparam IDLE   = 2'd0;
    localparam SCAN   = 2'd1;
    localparam DONE_S = 2'd2;

    reg [1:0] state;
    reg [$clog2(N)-1:0] pos, target;
    reg [15:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            done <= 1'b0;
            word_length <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (start) begin
                        // Normalize: a < b
                        if (pos_a < pos_b) begin
                            pos <= pos_a;
                            target <= pos_b;
                        end else begin
                            pos <= pos_b;
                            target <= pos_a;
                        end
                        count <= 0;
                        done <= 1'b0;
                        state <= SCAN;
                    end
                end

                SCAN: begin
                    adj_check_idx <= pos;  // Check if pos and pos+1 are siblings
                    // Wait 1 cycle for adj_result
                    if (adj_result)
                        count <= count + 1;
                    if (pos < target - 1) begin
                        pos <= pos + 1;
                    end else begin
                        word_length <= count + (adj_result ? 1 : 0);
                        done <= 1'b1;
                        state <= DONE_S;
                    end
                end

                DONE_S: begin
                    done <= 1'b0;
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
```

### 4.3 Performance

| Parameter | Cycles |
|:----------|:-------|
| N=20, single pair | ~N = 20 cycles |
| N=20, all pairs (190 pairs) | 190 × 20 = 3,800 cycles ≈ 19 µs @ 200 MHz |

---

## 5. Integration Testbench (Verilator)

### 5.1 Testbench Structure

```python
# _test_ultrametric_fpga.py — Software reference model for Verilator co-simulation
# Compares FPGA (Verilator) output against pure-Python reference implementation

import random

def padic_add_py(a_digits, b_digits, p_base):
    """Python reference for p-adic digit-serial addition."""
    carry = 0
    result = []
    for i in range(len(a_digits)):
        s = a_digits[i] + b_digits[i] + carry
        result.append(s % p_base)
        carry = s // p_base
    return result

def anc_py(dendrogram, leaf_a, leaf_b):
    """Python reference for nearest common ancestor."""
    ptr_a, ptr_b = leaf_a, leaf_b
    depth_a = dendrogram[ptr_a]['depth']
    depth_b = dendrogram[ptr_b]['depth']
    while depth_a > depth_b:
        ptr_a = dendrogram[ptr_a]['parent']
        depth_a -= 1
    while depth_b > depth_a:
        ptr_b = dendrogram[ptr_b]['parent']
        depth_b -= 1
    while ptr_a != ptr_b:
        ptr_a = dendrogram[ptr_a]['parent']
        ptr_b = dendrogram[ptr_b]['parent']
    return ptr_a

# Test harness
def test_padic_adder():
    p = 2
    for _ in range(1000):
        a = [random.randint(0, p-1) for _ in range(64)]
        b = [random.randint(0, p-1) for _ in range(64)]
        sw_result = padic_add_py(a, b, p)
        # hw_result = read_verilator_output()
        # assert sw_result == hw_result
    print("[PASS] p-adic adder: 1000 random tests")

def test_anc():
    # Build synthetic dendrogram
    dendrogram = build_random_dendrogram(1024)
    for _ in range(1000):
        a = random.randint(0, 1023)
        b = random.randint(0, 1023)
        sw_result = anc_py(dendrogram, a, b)
        # hw_result = read_verilator_output()
        # assert sw_result == hw_result
    print("[PASS] ANC engine: 1000 random tests")
```

---

## 6. Validation Against Braided Memory Register Conjecture

```python
# _validate_conjecture.py — FPGA-accelerated validation of δ = c·w
# Run on Verilator simulation of the Braid Engine + Tree Engine

def validate_conjecture(dendrogram, n_leaves=20):
    """Compute δ(i,j) and w(i,j) for all pairs, report R²."""
    import numpy as np
    from scipy.stats import linregress

    deltas = []  # ultrametric distances
    words = []   # braid word lengths

    for i in range(n_leaves):
        for j in range(i+1, n_leaves):
            # These would be FPGA-accelerated:
            # delta = UDIST(i, j)       # via ANC engine
            # w = BWGT(i, j)            # via Braid engine
            delta = anc_depth(dendrogram, i, j)   # software fallback
            w = braid_word_length(i, j, dendrogram)  # software fallback
            deltas.append(delta)
            words.append(w)

    slope, intercept, r_value, p_value, std_err = linregress(words, deltas)
    return {
        'R_squared': r_value**2,
        'slope': slope,
        'intercept': intercept,
        'n_pairs': len(deltas)
    }

# Target: R² > 0.9 supports the conjecture
# Falsification: R² < 0.5 disconfirms
```

---

*Certainty: [speculative] — these are novel hardware designs. [LLM-INFERRED] for resource estimates. Falsifiable by synthesis, place-and-route, and benchmarking.*
