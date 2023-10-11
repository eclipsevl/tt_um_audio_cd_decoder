// RS(32,28) decoder
// Syndrome calculator module
// Vladislav Knyazkov, October 2023
module rs_dec_syndrome_calc
(
    input        i_clk,
    input        i_resb,

    input        i_frame_sync,

    input [7:0]  i_data,
    input        i_data_sync,

    output [7:0] o_s0,
    output [7:0] o_s1,
    output [7:0] o_s2,
    output [7:0] o_s3,

    output       o_ready
);

// Sync and edge detection
reg [1:0] r_rx_rdy_sync;
wire w_rx_rdy;
always@(posedge i_clk)
begin
    r_rx_rdy_sync <= {r_rx_rdy_sync[0], i_data_sync};
end

assign w_rx_rdy = ^r_rx_rdy_sync;

// accumulators   
reg [7:0] reg0;
reg [7:0] reg1;
reg [7:0] reg2;
reg [7:0] reg3;

reg [4:0] r_byte_cntr;

wire [7:0] w_s0;
wire [7:0] w_s1;
wire [7:0] w_s2;
wire [7:0] w_s3;

wire [7:0] w_m0;
wire [7:0] w_m1;
wire [7:0] w_m2;
wire [7:0] w_m3;

gf256_sum xi_s0(.a(i_data), .b(reg0), .s(w_s0));
gf256_sum xi_s1(.a(i_data), .b(reg1), .s(w_s1));
gf256_sum xi_s2(.a(i_data), .b(reg2), .s(w_s2));
gf256_sum xi_s3(.a(i_data), .b(reg3), .s(w_s3));

gf256_mult xi_m0(.A(w_s0), .B(8'h01), .X(w_m0));
gf256_mult xi_m1(.A(w_s1), .B(8'h02), .X(w_m1));
gf256_mult xi_m2(.A(w_s2), .B(8'h04), .X(w_m2));
gf256_mult xi_m3(.A(w_s3), .B(8'h08), .X(w_m3));

always@(posedge i_clk or negedge i_resb)
begin
    if(!i_resb)
    begin
        reg0 <= 8'h00;
        reg1 <= 8'h00;
        reg2 <= 8'h00;
        reg3 <= 8'h00;

        r_byte_cntr <= 5'h00;
    end
    else
    begin
        // Is there a new symbol?
        if(w_rx_rdy)
        begin
            reg0 <= w_m0;
            reg1 <= w_m1;
            reg2 <= w_m2;
            reg3 <= w_m3;
        end
    end
end

assign o_s0 = reg0;
assign o_s1 = reg1;
assign o_s2 = reg2;
assign o_s3 = reg3;

assign o_ready = &r_byte_cntr;

endmodule
