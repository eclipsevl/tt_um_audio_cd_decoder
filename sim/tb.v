`timescale 1ns/100ps
module tb;

initial begin
  $display("ololo");
  #1000
  $finish;
end

endmodule