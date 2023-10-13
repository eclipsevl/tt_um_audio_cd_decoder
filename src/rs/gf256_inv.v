// GF(256) 1/a calculation
// Vladislav Knyazkov, October 2023

module gf256_inv(
    input i_clk,

    input [7:0] x,
    output [7:0] y
);

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

assign y = x254;

endmodule
