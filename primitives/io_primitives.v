// =============================================================================
// Generic I/O and Primitive Wrappers for Vendor-Agnostic Synthesis/Simulation
// =============================================================================
// Provides synthesizable behavioral definitions for generic LiteX blackboxes.
// Add this file to your Quartus/Vivado/Icarus project if the tool cannot
// resolve these primitives during elaboration or simulation.
// =============================================================================

`timescale 1ns / 1ps

// Bidirectional I/O buffer with tristate control
module IOBUF (
    input  T,   // Tristate control: 1 = high-Z, 0 = drive
    input  I,   // Data input (to pad)
    output O,   // Data output (from pad)
    inout  IO   // Bidirectional pad
);
    assign IO = T ? 1'bz : I;
    assign O  = IO;
endmodule

// Differential output buffer
module OBUFDS (
    input  I,   // Single-ended data input
    output O,   // Positive differential output
    output OB   // Negative differential output
);
    assign O  = I;
    assign OB = ~I;
endmodule

// Input buffer
module IBUF (
    input  I,   // Pad input
    output O    // Buffered output
);
    assign O = I;
endmodule

// Output buffer
module OBUF (
    input  I,   // Data input
    output O    // Pad output
);
    assign O = I;
endmodule

// Tristate output buffer
module OBUFT (
    input  T,   // Tristate control: 1 = high-Z, 0 = drive
    input  I,   // Data input
    output O    // Pad output
);
    assign O = T ? 1'bz : I;
endmodule

// D flip-flop with async preset, clock enable, and optional INIT parameter
module FDPE #(
    parameter INIT = 1'b0
) (
    input  D,    // Data input
    input  C,    // Clock (positive edge)
    input  CE,   // Clock enable (active high)
    input  PRE,  // Async preset (active high)
    output Q     // Registered output
);
    reg q_int = INIT;
    always @(posedge C or posedge PRE)
        if (PRE)     q_int <= 1'b1;
        else if (CE) q_int <= D;
    assign Q = q_int;
endmodule

// Lattice output flip-flop with async preset and OE
module OFS1P3BX (
    input  D,     // Data input
    input  SP,    // Clock (positive edge)
    input  PD,    // Async preset (active high)
    input  G,     // Output enable / tristate control (active low = drive)
    output Q      // Registered output
);
    reg q_int;
    always @(posedge SP or posedge PD)
        if (PD) q_int <= 1'b1;
        else    q_int <= D;
    assign Q = G ? q_int : 1'bz;
endmodule

// Lattice input flip-flop with async preset
module IFS1P3BX (
    input  D,     // Data input
    input  SP,    // Clock (positive edge)
    input  PD,    // Async preset (active high)
    input  G,     // Input enable (active low = sample)
    output Q      // Registered output
);
    reg q_int;
    always @(posedge SP or posedge PD)
        if (PD)      q_int <= 1'b1;
        else if (!G) q_int <= D;
    assign Q = q_int;
endmodule

// Lattice bidirectional buffer
module BB (
    input  T,     // Tristate control: 1 = high-Z, 0 = drive
    input  I,     // Data input
    output O,     // Data output
    inout  B      // Bidirectional pad
);
    assign B = T ? 1'bz : I;
    assign O = B;
endmodule
