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

    output [7:0] o_gg0,
    output [7:0] o_gg1,

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

wire [7:0] w_ma0;
wire [7:0] w_ma1;
wire [7:0] w_ma2;
wire [7:0] w_ma3;

wire [7:0] w_sb0;
wire [7:0] w_sb1;
wire [7:0] w_sb2;

reg [3:0] r_state;

reg       r_gf256_inv_start;
wire      w_gf256_inv_done;

wire [7:0] w_a3_inv;

localparam STATE_IDLE = 0;
localparam STATE_LOAD = 1;
localparam STATE_SUB_X2 = 5;
localparam STATE_SUB_X1 = 6;
localparam STATE_SUB_X0 = 7;
localparam STATE_DIV_DONE = 8;

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
            r_gf256_inv_start <= 1'b1;
            r_state <= STATE_SUB_X1;
          end

        STATE_SUB_X1:
          begin
            // substarct a*(inv(a3)*b3) from b
            // or B - A * kX
            if(w_gf256_inv_done)
            begin
                $display("Mult val: ", w_ma3);
                reg_b0 <= 8'h00;
                reg_b1 <= w_sb0;
                reg_b2 <= w_sb1;
                reg_b3 <= w_sb2;               
            end

            r_gf256_inv_start <= w_gf256_inv_done ?         1'b0 :         1'b0;
            r_state           <= w_gf256_inv_done ? STATE_SUB_X0 : STATE_SUB_X1;
          end
          
          STATE_SUB_X0:
          begin
            // substarct a*(inv(a3)*b3) from b
            // or B - A * k
            if(w_gf256_inv_done)
            begin
                $display("Mult val: ", w_ma3);
                reg_b0 <= 8'h00;
                reg_b1 <= w_sb0;
                reg_b2 <= w_sb1;
                reg_b3 <= w_sb2;
            end

            r_gf256_inv_start <= w_gf256_inv_done ?             1'b0 :         1'b0;
            r_state           <= w_gf256_inv_done ?   STATE_DIV_DONE : STATE_SUB_X0;
          end

          STATE_DIV_DONE:
          begin
            // first division b/a is done
            // check whether we are done or another iteration is required
            // Order of poly in reg b should be <2
            if(|reg_b2) 
            begin
                // Order is 2. Need to do swap and run another iteration
                reg_b0 <= reg_a0;
                reg_b1 <= reg_a1;
                reg_b2 <= reg_a2;
                reg_b3 <= reg_a3;  

                reg_a0 <= 8'h00;
                reg_a1 <= reg_b1;
                reg_a2 <= reg_b2;
                reg_a3 <= reg_b3;  

                r_state <= STATE_SUB_X1;
                r_gf256_inv_start <= 1'b1;
            end
            else
            begin
              // order is <2 
              r_state <= STATE_IDLE;
            end
          end

        default:
            r_state <= STATE_IDLE;
    endcase
end

// gf256_inv instance
gf256_inv xi_gf256_inv(
    .i_clk        (i_clk),

    .i_start      (r_gf256_inv_start),

    .x            (reg_a3),
    .y            (w_a3_inv),

    .o_ready      (w_gf256_inv_done)
);

gf256_mult xi_ma0(.A(w_ma3), .B(reg_a0), .X(w_ma0));
gf256_mult xi_ma1(.A(w_ma3), .B(reg_a1), .X(w_ma1));
gf256_mult xi_ma2(.A(w_ma3), .B(reg_a2), .X(w_ma2));
gf256_mult xi_ma3(.A(w_a3_inv), .B(reg_b3), .X(w_ma3));

gf256_sum xi_sb0(.a(w_ma0), .b(reg_b0), .s(w_sb0));
gf256_sum xi_sb1(.a(w_ma1), .b(reg_b1), .s(w_sb1));
gf256_sum xi_sb2(.a(w_ma2), .b(reg_b2), .s(w_sb2));

assign o_gg0 = reg_b2;
assign o_gg1 = reg_b3;
assign o_ready = r_state == STATE_IDLE;

always@(r_state)
begin
    $display("===============================================================");
    $display("FSM_STATE: %d", r_state);
    $display("a3\ta2\ta1\ta0\t\tb3\tb2\tb1\tb0");
    $display("%d\t%d\t%d\t%d\t\t%d\t%d\t%d\t%d", 
        reg_a3, reg_a2, reg_a1, reg_a0, reg_b3, reg_b2, reg_b1, reg_b0);

end

endmodule
