module blocksTest();
    input a;
    input b;
    input cond;
    input x;
  	output reg[3:0] c;
    reg[4:0] sum;
    reg[4:0] sub;
    

    initial
      begin
        c = a+b;
      end
    
    always @(a or b or c)
      begin
        if(a)
          begin
            cond = 3'b00X;
          end
        else
          begin
            sum = 1'b0;
          end
      end
    
endmodule;