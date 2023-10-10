`timescale 1ns/100ps
module tb;

reg clk = 0;

always@(*) clk <= #10 ~clk;

initial begin
  $dumpfile("tb.vcd");
  $dumpvars(0,tb);
  $display("ololo");
  #1000
  $finish;
end

endmodule