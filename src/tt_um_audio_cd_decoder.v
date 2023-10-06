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

efm_lut_decoder xi_efm_lut_decoder
(
  .i_efm_symb      ({ui_in, uio_in[5:0]}),
  .o_data          (uo_out),
	
  .o_s0_sync      (uio_out[0]),
  .o_s1_sync      (uio_out[1])
);
    
assign uio_oe = 8'h00;
assign uio_out[2:7] = 6'h00;

endmodule
