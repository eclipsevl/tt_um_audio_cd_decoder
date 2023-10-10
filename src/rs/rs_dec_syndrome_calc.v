// RS(32,28) decoder
// Syndrome calculator module
// Vladislav Knyazkov, October 2023
module rs_dec_syndrome_calc
(
    input        i_clk,
    input        i_resb,

    input        i_start,

    input [7:0]  i_rx,
    input        i_rx_en,

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
    r_rx_rdy_sync <= {r_rx_rdy_sync[0], i_rx_en}
end

w_rx_rdy = ^r_rx_rdy_sync;

// accumulators   
reg [7:0] reg0;
reg [7:0] reg1;
reg [7:0] reg2;
reg [7:0] reg3;

wire [7:0] w_mac0;
wire [7:0] w_mac1;
wire [7:0] w_mac2;
wire [7:0] w_mac3;

always@(posedge i_clk or negedge i_resb)
begin
    if(!i_resb)
    begin
        reg0 <= 8'h00;
        reg1 <= 8'h00;
        reg2 <= 8'h00;
        reg3 <= 8'h00;
    end
    else
    begin
        // Is there a new symbol?
        if(w_rx_rdy)
        begin
            reg0 <= w_mac0;
            reg1 <= w_mac1;
            reg2 <= w_mac2;
            reg3 <= w_mac3;
        end
    end
end

    while(cntr < n): 
        control = cntr < k  
        # There was a mistake in the textbook?
        s0 = gf_add(reg0, RX[cntr-n])
        m0 = gf_mult(s0, 1)     
        reg0 = m0
        #print(f"({reg0*control} + {RX[cntr-n]}) * {2} = {m0}, reg0 = {reg0}") 

        s1 = gf_add(reg1, RX[cntr-n])
        m1 = gf_mult(s1, 2)
        reg1 = m1

        s2 = gf_add(reg2, RX[cntr-n])
        m2 = gf_mult(s2, 4)
        reg2 = m2
    
        s3 = gf_add(reg3, RX[cntr-n])
        m3 = gf_mult(s3, 8)
        reg3 = m3
               

        cntr = cntr + 1

    #s0 = reg0
    if(verbose):
        print(f"syndrome: {s3, s2, s1, s0}")

endmodule
