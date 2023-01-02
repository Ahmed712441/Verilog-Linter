module fullader();
  input a;
  input b;
  input cin;
  reg out;
  output carry;
  reg[3:0] testvar;

  out = a^b^cin;
  carry = a&b | cin&a | cin&b;
  
  case(a)
    1'b0: begin
      out = carry;
    end
    1'b1: begin
      out = cin;
    end
  endcase

  casez(testvar)
    4'b1z11: begin
      out = carry;
    end
    4'b1011: begin
      out = cin;
    end
    4'bz111: begin
      out = cin;
    end
    4'b00zz: begin
      out = cin;
    end
    4'b0011: begin
      out = cin;
    end
    4'b000z: begin
      out = cin;
    end
  endcase


endmodule