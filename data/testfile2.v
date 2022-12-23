module arithmeticTest();
    input a;
    input b;
    input cond;
  	output[3:0] c;
  
    c = a+b;
    a = a+2'b11;
    cond = c;
    c = cond & a + b;

endmodule;