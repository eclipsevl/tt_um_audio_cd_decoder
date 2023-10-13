`timescale 1ns/100ps
module tb;

reg clk = 0;
reg resb = 0;

reg frame_sync = 0;
reg [7:0] data = 0;
reg data_sync = 0;
reg [4:0] count = 0;

always@(*) clk <= #10 ~clk;

reg [7:0] frame [31:0];// = {32, 24, 9, 58, 243, 130, 31, 203, 254, 63, 228, 105, 85, 191, 59, 146, 252, 226, 26, 0, 236, 76, 251, 132, 32, 182, 239, 187, 39, 43, 51, 254};


wire [7:0] w_s0;
wire [7:0] w_s1;
wire [7:0] w_s2;
wire [7:0] w_s3;

wire w_rdy;

reg [7:0] rg = 0;

rs_dec_syndrome_calc xi_rs_dec_syndrome_calc
(
    .i_clk(clk),
    .i_resb(resb),

    .i_frame_sync(frame_sync),

    .i_data(data),
    .i_data_sync(data_sync),

    .o_s0(w_s0),
    .o_s1(w_s1),
    .o_s2(w_s2),
    .o_s3(w_s3),

    .o_ready(w_rdy)
);


initial begin


  $dumpfile("tb.vcd");
  $dumpvars(0,tb);
  $display("Starting RS syndrome calculator test");
  #1000
  resb = 1;

  $display("Reset released");
  #1000
  @(posedge clk) 
  frame_sync = 1;
  @(posedge clk)
  frame_sync = 0;

  @(posedge clk);
  repeat (32) begin
    data = frame[count];
    count = count + 1;
    data_sync = ~data_sync;
    rg = rg ^ data;
    #1000
    $display("%d", count);
  end

  #1000
  $display("syndrome: (27, 203, 18, 121)\n %d, %d, %d, %d", w_s0, w_s1, w_s2, w_s3);
  $finish;
end

endmodule