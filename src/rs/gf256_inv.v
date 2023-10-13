// GF(256) 1/a calculation
// Vladislav Knyazkov, October 2023

module gf256_inv(
    input i_clk,

    input i_start,
    
    input [7:0] x,
    output [7:0] y
);

/*
wire [7:0] x2,x3,x4,x7,x8,x15,x30,x60,x120,x127,x254;	 
	 
gf256_mult MM1(.A(x),.B(x),.X(x2));
gf256_mult MM2(.A(x),.B(x2),.X(x3));
gf256_mult MM3(.A(x2),.B(x2),.X(x4));
gf256_mult MM4(.A(x3),.B(x4),.X(x7));
gf256_mult MM5(.A(x4),.B(x4),.X(x8));
gf256_mult MM6(.A(x7),.B(x8),.X(x15));
gf256_mult MM7(.A(x15),.B(x15),.X(x30));
gf256_mult MM8(.A(x30),.B(x30),.X(x60));
gf256_mult MM9(.A(x60),.B(x60),.X(x120));
gf256_mult MM10(.A(x7),.B(x120),.X(x127));
gf256_mult MM11(.A(x127),.B(x127),.X(x254));
*/

reg [7:0] r_squares;
reg [7:0] r_acc;

wire [7:0] w_m0_in, w_m0_out, w_m1_out;

assign w_m0_in = i_start ? x : r_squares;
gf256_mult xi_m0(.A(w_m0_in),.B(w_m0_in),.X(w_m0_out));
gf256_mult xi_m2(.A(w_m0_out),.B(r_acc),.X(w_m1_out));

always@(posedge i_clk)
begin
    r_squares <= w_m0_out;
    r_acc <= i_start ? 8'h01 : w_m1_out;
end

assign y = r_acc;

endmodule
