// RS(32,28) decoder
// Euclid algorith implementation
// Error locator/magnitude poly calculation
// Vladislav Knyazkov, October 2023

module rs_dec_euclid_alg
(
    input        i_clk,
    input        i_resb,

    input        i_synd_sync,

    input  [7:0] i_s0,
    input  [7:0] i_s1,
    input  [7:0] i_s2,
    input  [7:0] i_s3,

    output       o_ready
);

reg [7:0] reg_a0;
reg [7:0] reg_a1;
reg [7:0] reg_a2;
reg [7:0] reg_a3;

reg [7:0] reg_b0;
reg [7:0] reg_b1;
reg [7:0] reg_b2;
reg [7:0] reg_b3;

reg [3:0] r_state;

reg       r_gf256_inv_start;
wire      w_gf256_inv_done;

localparam STATE_IDLE = 0;
localparam STATE_LOAD = 1;
localparam STATE_SUB_X = 5;

always@(posedge i_clk)
begin
    case(r_state)
        STATE_IDLE:
            r_state <= i_synd_sync ? STATE_LOAD : STATE_IDLE;

        STATE_LOAD:
          begin
            // load syndrome into register a (divisor)
            reg_a0 <= i_s0;
            reg_a1 <= i_s1;
            reg_a2 <= i_s2;
            reg_a3 <= i_s3;

            // load dividend into register b (x^4)
            reg_b0 <= 8'h00;
            reg_b1 <= 8'h00;
            reg_b2 <= 8'h00;
            reg_b3 <= 8'h01;
            
            // start calculation inv(a3) for next state
            r_state <= i_synd_sync ? STATE_LOAD : STATE_SUB_X;
          end

        STATE_SUB_X:
          begin
            // substarct a*(inv(a3)*b3) from b
            if(w_gf256_inv_done)
            begin
                //reg_b1 <= w_sb0;
                //reg_b2 <= w_sb1;
                //reg_b3 <= w_sb2;               
            end

            r_state <= STATE_IDLE;
          end
        default:
            r_state <= STATE_IDLE;
    endcase
end

always@(r_state)
begin
    $display("===============================================================");
    $display("FSM_STATE: %d", r_state);
    $display("a3\ta2\ta1\ta0\t\tb3\tb2\tb1\tb0");
    $display("%d\t%d\t%d\t%d\t\t%d\t%d\t%d\t%d", 
        reg_a3, reg_a2, reg_a1, reg_a0, reg_b3, reg_b2, reg_b1, reg_b0);

end

endmodule
