// GF(256) summator
// Vladislav Knyazkov, October 2023

module gf256_sum(
    input [7:0] a,
    input [7:0] b,

    output [7:0] s
);

assign s = a^b;

endmodule