// GF(256) 1/a calculation
// Vladislav Knyazkov, October 2023

module gf256_inv(
    input i_clk,

    input i_start,

    input [7:0] x,
    output [7:0] y,

    output o_ready
);

reg [7:0] r_squares;
reg [7:0] r_acc;
reg [3:0] r_cntr;

wire [7:0] w_m0_in, w_m0_out, w_m1_out;

assign w_m0_in = i_start ? x : r_squares;
gf256_mult xi_m0(.A(w_m0_in),.B(w_m0_in),.X(w_m0_out));
gf256_mult xi_m2(.A(r_squares),.B(r_acc),.X(w_m1_out));

always@(posedge i_clk)
begin
    r_squares <= w_m0_out;
    r_acc <= i_start ? 8'h01 : w_m1_out;
    r_cntr <= i_start ? 3'h0 : 
        r_cntr === 7 ? r_cntr : r_cntr + 1;
end

assign y = r_acc;
assign o_ready = r_cntr === 7; 

endmodule
