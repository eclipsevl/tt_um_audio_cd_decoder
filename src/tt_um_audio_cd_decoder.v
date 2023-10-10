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

reg  [7:0] reg0;
wire [7:0] w_mult_out;

gf256_mult xi_mult(.A(ui_in), .B(uio_in), .X(w_mult_out));

always@(posedge clk or negedge rst_n)
begin
    if(!rst_n)
        reg0 <= 8'h00;
    else
        reg0 <= w_mult_out;
end

assign uio_oe = 8'h00;
assign uio_out = 8'h00;
assign uo_out = reg0;

endmodule
