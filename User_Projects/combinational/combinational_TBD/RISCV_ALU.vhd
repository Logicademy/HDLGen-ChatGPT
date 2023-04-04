-- Engineer: Fearghal Morgan, Arthur Beretta, Joseph Clancy
-- National University of Ireland Galway
-- 
-- Module Name: RISCV_ALU
-- Description: Execution arithmetic and logic unit module of RISC-V processor
--
-- Signal dictionary https://www.vicilogic.com/static/ext/RISCV/RISCVici/RISCVici_SignalDictionary.pdf
-- 
-- Generates ALUOut from ALU data inputs A, B and control input selALUOP(3:0)
-- Operations include   arithmetic,   logical,   shift (immediate or registered),   set less than  
--
-- Generates branch: asserted when branch instruction 
--
-- Arithmetic operations on std_logic_vector (slv) types
-- Requires 
--   1. Selection of arithmetic library, "use IEEE.NUMERIC_STD.ALL;" used in VHDL library section. 
--   IEEE.NUMERIC_STD.vhd https://www.csee.umbc.edu/portal/help/VHDL/packages/cieee/numeric_std.vhd supports -/+ functions 
--     Id: A.2
--      function "-" (ARG: SIGNED) return SIGNED;
--      Result subtype: SIGNED(ARG'LENGTH-1 downto 0). Result: Returns the value of the unary minus operation on a SIGNED vector ARG.
--     Id: A.4
--      function "+" (L, R: SIGNED) return SIGNED;
--      Result subtype: SIGNED(MAX(L'LENGTH, R'LENGTH)-1 downto 0). Result: Adds two SIGNED vectors that may be of different lengths.
--   2. type conversion of slv, i.e, signed or unsigned
--   3. arithmetic operation, using arithmetic operator, e.g, +, -
--   4. type conversion of arithmetic result to slv 
--  Examples:
--      signed addition:    std_logic_vector(signed(A) + signed(B));
--      signed subtraction: std_logic_vector(signed(A) - signed(B));
--
--  Shift left/right VHDL : refer to numeric_std.vhd (link above), search for 'shift'  functions
--
--  Branch: refer to numeric_std.vhd library: =  /=    <    >=    <   >=
--  Assert signal branch for branch instructions (selALUOP = 0b1010-0b1111)  
--  Equality check requires type conversion of std_logic_vector (slv) signal to signed or unsigned
--  Equal =    or  not equal /=  check does not required slv type conversion   
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity RISCV_ALU is
  Port (A        : in  std_logic_vector(31 downto 0); -- ALU 32-bit input A
        B        : in  std_logic_vector(31 downto 0); -- ALU 32-bit input B
        selALUOp : in  std_logic_vector( 3 downto 0); -- ALU operation select 
		ALUOut   : out std_logic_vector(31 downto 0); -- ALU 32-bit output
        branch   : out std_logic                      -- assert on branch if condition is TRUE 
        );        
end RISCV_ALU;

architecture comb of RISCV_ALU is
begin

ALUOut_branch_i: process(A, B, selALUOp) -- ALU process
begin
    ALUOut <= (others => '0'); -- Default assignment
    branch <= '0';  
    case selALUOp is 
    
      -- arithmetic operation 
      when "0000" => ALUOut <= std_logic_vector(signed(A) + signed(B)); -- ADD
      when "0001" => ALUOut <= std_logic_vector(signed(A) - signed(B)); -- SUB

      -- logical operation
      when "0010" => ALUOut <= A and B; -- AND
      when "0011" => ALUOut <= A or  B; -- OR
      when "0100" => ALUOut <= A xor B; -- XOR

      --  shift (immediate or registered) operation
      when "0101" => ALUOut <= std_logic_vector( shift_left (unsigned(A), to_integer( unsigned(B(4 downto 0))) ) ); -- Shift left logical (SLL)
      when "0110" => ALUOut <= std_logic_vector( shift_right(unsigned(A), to_integer( unsigned(B(4 downto 0))) ) ); -- Shift right logical (SRA)
      when "0111" => ALUOut <= std_logic_vector( shift_right(signed  (A), to_integer( unsigned(B(4 downto 0))) ) ); -- Shift right arithmetic (SRA)

      -- set less than operations
	  when "1000" => -- Set less than immediate (SLT) 
        if signed(A)   < signed(B)   then 
					 ALUOut(0) <= '1'; end if; 
	  when "1001" => -- Set less than unsigned (SLTU)
        if unsigned(A) < unsigned(B) then 
					 ALUOut(0) <= '1'; end if; 

	  -- Branch check 
	  when "1010" => if A = B             		   then branch <= '1'; end if; -- BEQ						
      when "1011" => if A /= B 			           then branch <= '1'; end if; -- BNE	
      when "1100" => if signed(A)   <  signed(B)   then branch <= '1'; end if; -- BLT
      when "1101" => if signed(A)   >= signed(B)   then branch <= '1'; end if; -- BGE
      when "1110" => if unsigned(A) <  unsigned(B) then branch <= '1'; end if; -- BLTU 					
      when "1111" => if unsigned(A) >= unsigned(B) then branch <= '1'; end if; -- BGEU

      when others => null;
    end case;
end process;

end comb;