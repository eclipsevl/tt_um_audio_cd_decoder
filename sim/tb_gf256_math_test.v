`timescale 1ns/100ps
module tb;

reg clk = 0;
reg resb = 0;

reg start = 0;
reg [7:0] data = 0;

always@(*) clk <= #10 ~clk;


wire [7:0] w_data_inv;
wire [7:0] w_mult_out;

wire w_rdy;

gf256_inv xi_gf256_inv(
    .i_clk(clk),

    .i_start(start),
    .o_ready(w_rdy),

    .x(data),
    .y(w_data_inv)
);

gf256_mult xi_gf256_mult(
    .A(data),
    .B(w_data_inv),

    .X(w_mult_out)
);


initial begin


  $dumpfile("tb.vcd");
  $dumpvars(0,tb);
  $display("Starting RS syndrome calculator test");
  #1000
  resb = 1;

  $display("Reset released");
  #1000

  data = 1;

  
  repeat (255) begin
    @(posedge clk);
    #1
    start = 1;
    @(posedge clk)
    #1
    start = 0;

    @(posedge w_rdy);
    #1
    $display("x = %d, inv_x = %d, x*inv_x = %d", data, w_data_inv, w_mult_out);
    #1000
    data = data + 1;
    
  end

  /*
  x2: 4
x4: 16
x8: 29
x16: 76
x32: 157
x64: 95
x128: 133
x6: 64
x14: 19
x30: 96
x62: 222
x126: 102
*/

  #1000
  $finish;
end

endmodule