module fullader();
  input[3:0] a;
  output out;
  
  reg[2:0] state = 3'b000;  

  case(state)
    3'b000: begin
      state = 3'b001;
    end
    3'b001: begin
      state = 3'b011;
    end
    3'b011: begin
      state = 3'b011;
    end
    3'b100: begin
      state = 3'b011;
    end
  endcase


endmodule