`timescale 1ns/100ps
module tb;

reg clk = 0;
reg resb = 0;

reg synd_sync = 0;

always@(*) clk <= #10 ~clk;

wire [7:0] w_s0;
wire [7:0] w_s1;
wire [7:0] w_s2;
wire [7:0] w_s3;

assign w_s0 = 8'd1;
assign w_s1 = 8'd2;
assign w_s2 = 8'd4;
assign w_s3 = 8'd8;

wire w_rdy;

reg [7:0] rg = 0;

rs_dec_euclid_alg xi_rs_dec_euclid_alg
(
    .i_clk(clk),
    .i_resb(resb),

    .i_synd_sync(synd_sync),

    .i_s0(w_s0),
    .i_s1(w_s1),
    .i_s2(w_s2),
    .i_s3(w_s3),

    .o_ready(w_rdy)
);


initial begin


  $dumpfile("tb.vcd");
  $dumpvars(0,tb);
  $display("Starting euclid alg test");
  #1000
  resb = 1;

  $display("Reset released");
  #1000
  @(posedge clk) 
  synd_sync = 1;
  @(posedge clk)
  synd_sync = 0;

 

  #10000
  $finish;
end

endmodule