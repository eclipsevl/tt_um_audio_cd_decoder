// GF(256) 1/a calculation
// Vladislav Knyazkov, October 2023

module gf256_inv(
    input [7:0] a,
    output [7:0] x
);

assign x = a^a;

endmodule
