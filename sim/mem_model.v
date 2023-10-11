module mem_model(
    input i_clk,
    input i_cs,
    input i_read,
    input i_write,
    input [11:0] i_addr
    input [7:0] io_data
)

always@(posedge i_clk)
begin
    if(i_write)
       mem[i_addr] <= io_data;
    else if(i_read)
    begin
       r_out_end <= 1'b1;
       r_out <= mem[i_addr];
    end
       
end

endmodule