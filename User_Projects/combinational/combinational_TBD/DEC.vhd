-- Engineer: Fearghal Morgan 
-- National University of Ireland Galway
-- 
-- Module Name: DEC
-- Description: Instruction Decoder Module for the RV32I RISC-V Processor

-- Signal dictionary https://www.vicilogic.com/static/ext/RISCV/RISCVici/RISCVici_SignalDictionary.pdf

-- instruction format (RISC-V Spec) https://www.vicilogic.com/static/ext/RISCV/riscv-spec.pdf#page=146
--  I-type format: imm[11:0] 					rs1	f3				rd 	opcode 
--  R-type format: f7                    rs2	rs1	f3				rd 	opcode 
--  S-type format: imm[11:5] 			 rs2    rs1 f3 imm[4:0] 		opcode                       
--  B-type format: imm[12¦10:5] 		 rs2    rs1 f3 imm[4:1¦11]   	opcode
--  U-type format: imm[31:12] 										rd 	opcode 
--  J-type format: imm[20¦10:1¦11¦19:12] 							rd 	opcode

-- XX_ signal prefix, if used, excludes the signal from the vicilogic signal view list during vicilogic RISC-V VHDL model parsing

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity DEC is
  Port (instruction : in  std_logic_vector(31 downto 0);
        branch      : in  std_logic;
		extImm      : out std_logic_vector(31 downto 0);
		rs1         : out std_logic_vector( 4 downto 0);
		rs2         : out std_logic_vector( 4 downto 0);
		RWr         : out std_logic;
		rd          : out std_logic_vector( 4 downto 0);
		selPCSrc    : out std_logic;
		jalr        : out std_logic;
		auipc       : out std_logic;
		selALUBSrc  : out std_logic;
		selALUOp    : out std_logic_vector( 3 downto 0);
		selDToM     : out std_logic_vector( 1 downto 0);
		MWr         : out std_logic;
		MRd         : out std_logic;
		selDFrM     : out std_logic_vector( 2 downto 0);
		selWBD      : out std_logic_vector( 1 downto 0);
        instrID     : out std_logic_vector( 5 downto 0) 
		);
end DEC;

architecture combinational of DEC is
signal opcode         : std_logic_vector( 6 downto 0);
signal f3             : std_logic_vector( 2 downto 0);
signal f7             : std_logic_vector( 6 downto 0);
signal opcode_f3_f7_5 : std_logic_vector(10 downto 0);    
signal XX_DEC_vector  : std_logic_vector(70 downto 0); -- assign 71 bit vector for selected opcode, f3, f7 combinations

-- ====== signals used in XX_DEC_vector generation
-- constants
signal XX_bitEq0      : std_logic := '0';             
signal XX_bitEq1      : std_logic := '1';
-- immediate signals generate from instruction fields
signal XX_imm_I_12    : std_logic_vector(11 downto 0);
signal XX_imm_S_12    : std_logic_vector(11 downto 0);
signal XX_imm_B_13    : std_logic_vector(12 downto 0);
signal XX_imm_U_32    : std_logic_vector(31 downto 0);
signal XX_imm_J_21    : std_logic_vector(20 downto 0);
-- sign-extend imm to 32-bits
signal XX_extImm_I    : std_logic_vector(31 downto 0);
signal XX_extImm_S    : std_logic_vector(31 downto 0);
signal XX_extImm_B    : std_logic_vector(31 downto 0);
signal XX_extImm_U    : std_logic_vector(31 downto 0);
signal XX_extImm_J    : std_logic_vector(31 downto 0);

begin 

-- assemble extended immediate signal combinations. Use in generation of XX_DEC_vector
imm_I_i:    XX_imm_I_12 <= instruction(31 downto 20); 							
imm_S_i:    XX_imm_S_12 <= instruction(31 downto 25) & instruction(11 downto 7); 
imm_B_i:    XX_imm_B_13 <= instruction(31) & instruction(7) & instruction(30 downto 25) & instruction(11 downto 8) & '0'; 
imm_U_i:    XX_imm_U_32 <= instruction(31 downto 12) & X"000"; 
imm_J_i:    XX_imm_J_21 <= instruction(31) & instruction(19 downto 12) & instruction(20) & instruction(30 downto 21) & '0'; 
extImm_I_i: XX_extImm_I <= std_logic_vector(  resize( signed(XX_imm_I_12), instruction'length )  ); 
extImm_S_i: XX_extImm_S <= std_logic_vector(  resize( signed(XX_imm_S_12), instruction'length )  ); 
extImm_B_i: XX_extImm_B <= std_logic_vector(  resize( signed(XX_imm_B_13), instruction'length )  ); 
extImm_U_i: XX_extImm_U <= std_logic_vector(  resize( signed(XX_imm_U_32), instruction'length )  ); 
extImm_J_i: XX_extImm_J <= std_logic_vector(  resize( signed(XX_imm_J_21), instruction'length )  ); 


-- generate instruction opcode field 
opcode_i: opcode <= instruction( 6 downto 0);

-- generate instruction f3 field
f3_i: process (instruction) 
begin
    f3  <= instruction(14 downto 12);  -- default
    if instruction(6 downto 0) = "0110111" or  instruction(6 downto 0) = "0010111" or  instruction(6 downto 0) = "1101111" then 
   	  f3 <= "000";
	end if;
end process;

-- generate instruction f7 field
f7_i: process (instruction) 
begin
    f7 <= "0000000"; -- default
	if instruction(6 downto 0) = "0010011" then
       if instruction(14 downto 12) = "001" or instruction(14 downto 12) = "101" then 
          f7  <= instruction(31 downto 25); 
       elsif instruction(6 downto 0) = "0110011" then
          f7  <= instruction(31 downto 25); 
	   end if;
	end if;
end process;

-- Combine opcode, f3 and f7(5) and use in generation of XX_DEC_vector 
opcode_f3_f7_5 <= opcode & f3 & f7(5); -- 7 + 3 + 1 = 11 bits

-- generate XX_DEC_vector
DEC_i: process (opcode_f3_f7_5, 
                instruction, branch, XX_extImm_I, XX_extImm_S, XX_extImm_B, XX_extImm_U, XX_extImm_J, XX_bitEq1, XX_bitEq0) 
begin
XX_DEC_vector <=  (others => '0'); -- default assignment
-- Signal names aligned to values        instrID     rs1	                     rs2	                  RWr	         rd	                  extImm	 selPCSrc	 jalr  auipc selALUBSrc  selALUOp selDToM  MWr   MRd   DFrM   selWBD
case opcode_f3_f7_5 is                                                                                                                                                                    
 when "01101110000" => XX_DEC_vector <= "000001" & "00000"                   & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_U & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '0' & "000" & "00"; --  U-type. Instruction LUI
 when "00101110000" => XX_DEC_vector <= "000010" & "00000"                   & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_U & XX_bitEq0 & '0' & '1' & '0'        & "0000" & "00" & '0' & '0' & "000" & "00"; --  U-type. Instruction AUIPC
																																													         
 when "11011110000" => XX_DEC_vector <= "000011" & "00000"                   & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_J & XX_bitEq1 & '0' & '0' & '0'        & "0000" & "00" & '0' & '0' & "000" & "10"; --  J-type. Instruction JAL
-- FM TBD : update instrID to have JALR value = 3 and ripple through other instrID values. Check if any consequences though                                                                  
 when "11001110000" => XX_DEC_vector <= "000100" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq1 & '1' & '0' & '0'        & "0000" & "00" & '0' & '0' & "000" & "10"; --  I-type. Instruction JALR
																																													         
 when "11000110000" => XX_DEC_vector <= "000101" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1010" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BEQ
 when "11000110010" => XX_DEC_vector <= "000110" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1011" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BNE
 when "11000111000" => XX_DEC_vector <= "000111" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1100" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BLT
 when "11000111010" => XX_DEC_vector <= "001000" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1101" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BGE
 when "11000111100" => XX_DEC_vector <= "001001" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1110" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BLTU
 when "11000111110" => XX_DEC_vector <= "001010" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_B & branch    & '0' & '0' & '1'        & "1111" & "00" & '0' & '0' & "000" & "00"; --  B-type. Instruction BGEU
																																													         
 when "00000110000" => XX_DEC_vector <= "001011" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '1' & "010" & "01"; --  I-type. Instruction LB
 when "00000110010" => XX_DEC_vector <= "001100" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '1' & "001" & "01"; --  I-type. Instruction LH
 when "00000110100" => XX_DEC_vector <= "001101" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '1' & "000" & "01"; --  I-type. Instruction LW
 when "00000111000" => XX_DEC_vector <= "001110" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '1' & "100" & "01"; --  I-type. Instruction LBU
 when "00000111010" => XX_DEC_vector <= "001111" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '1' & "011" & "01"; --  I-type. Instruction LHU
																																													         
 when "01000110000" => XX_DEC_vector <= "010000" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_S & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "10" & '1' & '0' & "000" & "00"; --  S-type. Instruction SB
 when "01000110010" => XX_DEC_vector <= "010001" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_S & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "01" & '1' & '0' & "000" & "00"; --  S-type. Instruction SH
 when "01000110100" => XX_DEC_vector <= "010010" & instruction(19 downto 15) & instruction(24 downto 20) & '0' & "00000"                  & XX_extImm_S & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '1' & '0' & "000" & "00"; --  S-type. Instruction SW
																																													         
 when "00100110000" => XX_DEC_vector <= "010011" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0000" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction ADDI
 when "00100110100" => XX_DEC_vector <= "010100" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "1000" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction SLTI
 when "00100110110" => XX_DEC_vector <= "010101" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "1001" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction SLTIU
 when "00100111000" => XX_DEC_vector <= "010110" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0100" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction XORI
 when "00100111100" => XX_DEC_vector <= "010111" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0011" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction ORI
 when "00100111110" => XX_DEC_vector <= "011000" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0010" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction ANDI
																																													         
 when "00100110010" => XX_DEC_vector <= "011001" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0101" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction SLLI
 when "00100111010" => XX_DEC_vector <= "011010" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0110" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction SRLI
 when "00100111011" => XX_DEC_vector <= "011011" & instruction(19 downto 15) & "00000"                   & '1' & instruction(11 downto 7) & XX_extImm_I & XX_bitEq0 & '0' & '0' & '0'        & "0111" & "00" & '0' & '0' & "000" & "00"; --  I-type. Instruction SRAI
																																													         
 when "01100110000" => XX_DEC_vector <= "011100" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0000" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction ADD 
 when "01100110001" => XX_DEC_vector <= "011101" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0001" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SUB
 when "01100110010" => XX_DEC_vector <= "011110" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0101" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SLL 
 when "01100110100" => XX_DEC_vector <= "011111" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "1000" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SLT
 when "01100110110" => XX_DEC_vector <= "100000" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "1001" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SLTU
 when "01100111000" => XX_DEC_vector <= "100001" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0100" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction XOR 
 when "01100111010" => XX_DEC_vector <= "100010" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0110" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SRL  
 when "01100111011" => XX_DEC_vector <= "100011" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0111" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction SRA  
 when "01100111100" => XX_DEC_vector <= "100100" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0011" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction OR 
 when "01100111110" => XX_DEC_vector <= "100101" & instruction(19 downto 15) & instruction(24 downto 20) & '1' & instruction(11 downto 7) & X"00000000" & XX_bitEq0 & '0' & '0' & '1'        & "0010" & "00" & '0' & '0' & "000" & "00"; --  R-type. Instruction AND 
when others => null;
end case;
end process;

instrID    <= XX_DEC_vector(70 downto 65); -- instruction identifier. Aids instruction indexing in HDL model

-- generate decoder output signals from DEC_vector
rs1        <= XX_DEC_vector(64 downto 60);
rs2        <= XX_DEC_vector(59 downto 55);
RWr        <= XX_DEC_vector(54);
rd         <= XX_DEC_vector(53 downto 49);
extImm     <= XX_DEC_vector(48 downto 17);
selPCSrc   <= XX_DEC_vector(16);
jalr       <= XX_DEC_vector(15);  
auipc      <= XX_DEC_vector(14);
selALUBSrc <= XX_DEC_vector(13);
selALUOp   <= XX_DEC_vector(12 downto  9);
selDToM    <= XX_DEC_vector( 8 downto  7);
MWr        <= XX_DEC_vector( 6);
MRd        <= XX_DEC_vector( 5);
selDFrM    <= XX_DEC_vector( 4 downto  2);
selWBD     <= XX_DEC_vector( 1 downto  0);

end combinational;