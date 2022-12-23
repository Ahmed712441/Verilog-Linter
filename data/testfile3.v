module fullader ();
  input a;
  input b;
  input cin;
  output out;
  inout carry;
  
  assign out = a^b^cin;
  assign carry = (a&b) | (cin&a) | (cin&b);
  
endmodule