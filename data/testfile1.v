module andOnCondution();
    input a;
    input b;
    input cond;
  	output reg [3:0] c;
    reg [16:0] m;
  initial
    begin
    	c=1'b0;
    end
  
  always @ (a or b or cond)
    begin
      if(cond === 1)
        begin
        	c = a&b;
        end
      else
        c = 1;
    end
  
endmodule;