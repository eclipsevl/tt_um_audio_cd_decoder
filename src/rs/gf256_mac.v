// GF(256) multiplier + accumulator
// Vladislav Knyazkov, October 2023

module gf256_mac(
    input [7:0] a,
    input [7:0] b,
    input [7:0] c,

    output [7:0] s
)

wire [7:0] w_mult;
gf256_mult xi_mult(.A(a), .B(b), .X(w_mult));
gf256_sum xi_sum(.a(w_mult), .b(c), .s(s));

endmodule