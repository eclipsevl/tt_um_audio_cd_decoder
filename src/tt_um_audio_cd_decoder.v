module tt_um_audio_cd_decoder (
`ifdef USE_POWER_PINS
  input VPWR,
  input VGND,
`endif
  input  wire [7:0] ui_in,   // Dedicated inputs
  output wire [7:0] uo_out,  // Dedicated outputs
  input  wire [7:0] uio_in,  // IOs: Input path
  output wire [7:0] uio_out, // IOs: Output path
  output wire [7:0] uio_oe,  // IOs: Enable path (active high: 0=input, 1=output)
  input  wire       ena,
  input  wire       clk,
  input  wire       rst_n
);

wire [7:0] w_s0;
wire [7:0] w_s1;
wire [7:0] w_s2;
wire [7:0] w_s3;

wire w_rdy;

reg [31:0] r_latch;

rs_dec_syndrome_calc xi_rs_dec_syndrome_calc
(
    .i_clk(clk),
    .i_resb(rst_n),

    .i_frame_sync(ena),

    .i_data(ui_in),
    .i_data_sync(uio_in[0]),

    .o_s0(w_s0),
    .o_s1(w_s1),
    .o_s2(w_s2),
    .o_s3(w_s3),

    .o_ready(w_rdy)
);

always@(posedge clk)
begin
  if(w_rdy)
    r_latch <= {w_w3, w_s2, w_s1, w_s0};
  else
    r_latch <= {r_latch[23:0], 8'h00;}
end

assign uio_oe = r_latch[31:24];
assign uio_out = 8'h00;
assign uo_out = 8'h00;

endmodule
