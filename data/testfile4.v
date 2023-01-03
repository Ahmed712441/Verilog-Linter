module busTest();
    input a;
    input b;
    input cond;
    input x;
  	output reg[3:0] c;
    reg[4:0] sum;
    reg[4:0] sub;
    output[2:0] out1;

    initial
      begin
        c = a+b;
      end
    
    always @(a or b or c)
      begin
        sub = 4'b0000;
        if(a)
          begin
            sum[2:4] = 3'b00X;
          end
        else
          begin
            sum = 1'b0;
          end
      end

    c = 3b'001+3b'100;
    out1[1] = 2'b00; 
    out1[1] = 1'b0;
    
endmodule;