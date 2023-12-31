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

wire [7:0] w_rx_data;

wire [7:0] w_s0;
wire [7:0] w_s1;
wire [7:0] w_s2;
wire [7:0] w_s3;

wire [7:0] w_gg0;
wire [7:0] w_gg1;

wire [7:0] w_gl0;
wire [7:0] w_gl1;
wire [7:0] w_gl2;

wire w_rdy;
wire w_euclid_rdy;


reg [31:0] r_latch;

efm_lut_decoder xi_efm_lut_decoder
(
  .i_efm_symb({ui_in, uio_in[7:2]}),
  .o_data(w_rx_data),
  
  .o_s0_sync(),
  .o_s1_sync()
);

rs_dec_syndrome_calc xi_rs_dec_syndrome_calc
(
    .i_clk(clk),
    .i_resb(rst_n),

    .i_frame_sync(ena),

    .i_data(w_rx_data),
    .i_data_sync(uio_in[0]),

    .o_s0(w_s0),
    .o_s1(w_s1),
    .o_s2(w_s2),
    .o_s3(w_s3),

    .o_ready(w_rdy)
);

rs_dec_euclid_alg xi_rs_dec_euclid_alg
(
    .i_clk(clk),
    .i_resb(rst_n),

    .i_synd_sync(w_rdy),

    .i_s0(w_s0),
    .i_s1(w_s1),
    .i_s2(w_s2),
    .i_s3(w_s3),

    .o_gg0(w_gg0),
    .o_gg1(w_gg1),

    .o_gl0(w_gl0),
    .o_gl1(w_gl1),
    .o_gl2(w_gl2),

    .o_ready(w_euclid_rdy)
);
/*
always@(posedge clk)
begin
  if(w_rdy)
    r_latch <= {w_s3, w_s2, w_s1, w_s0};
  else
    r_latch <= {r_latch[23:0], 8'h00};
end
*/

assign uio_oe = {w_euclid_rdy, 7'h00};
assign uio_out = w_gl0^w_gl1^w_gl2;
assign uo_out = w_gg1^w_gg0;

endmodule
