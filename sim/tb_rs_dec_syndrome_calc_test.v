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
       frame[0] = 32;
        frame[1] = 24;
        frame[2] = 9;
        frame[3] = 58;
        frame[4] = 243;
        frame[5] = 130;
        frame[6] = 31;
        frame[7] = 203;
        frame[8] = 254;
        frame[9] = 63;
        frame[10] = 228;
        frame[11] = 105;
        frame[12] = 85;
        frame[13] = 191;
        frame[14] = 59;
        frame[15] = 146;
        frame[16] = 252;
        frame[17] = 226;
        frame[18] = 26;
        frame[19] = 0;
        frame[20] = 236;
        frame[21] = 76;
        frame[22] = 251;
        frame[23] = 132;
        frame[24] = 32;
        frame[25] = 182;
        frame[26] = 239;
        frame[27] = 187;
        frame[28] = 39;
        frame[29] = 43;
        frame[30] = 51;
        frame[31] = 254;

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