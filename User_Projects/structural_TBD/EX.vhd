--  Model name		EX
--  Description		RISC-V processor execute stage, generating 32-bit values ALUOut, DToM and brAdd, and branch signal
--  Author(s)		Fearghal Morgan, Arthur Beretta, Joseph Clancy
--  Company			National University of Ireland, Galway 
--  Date			2nd Oct 2021
--  Change History 	Initial version

--  Signal dictionary 
-- 	https://www.vicilogic.com/static/ext/RISCV/RISCVici/RISCVici_SignalDictionary.pdf

-- internal signals 
-- A			ALU input A
-- B			ALU input B
-- brBase Add  	branch base addres

-- processes 
--  selA_i: 		Select ALU operand B
--  selB_i: 		Select ALU operand B
--  DToM_i: 		generate data for memory store  
--  brBaseAdd_i:	geberate branch base address 
--  genbrAdd_i: 	generate branch address 

-- components
--  ALU_i:  		ALU component  

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.ALL;

entity EX is
  Port (extImm     : in  std_logic_vector(31 downto 0); 
		rs1D       : in  std_logic_vector(31 downto 0);
        rs2D       : in  std_logic_vector(31 downto 0);
        jalr       : in  std_logic;                    
        PC         : in  std_logic_vector(31 downto 0);
        auipc      : in  std_logic;                    
        selALUBSrc : in  std_logic;  
        selALUOp   : in  std_logic_vector( 3 downto 0);  
        selDToM    : in  std_logic_vector( 1 downto 0); 
        ALUOut     : out std_logic_vector(31 downto 0);
        DToM       : out std_logic_vector(31 downto 0);
        brAdd      : out std_logic_vector(31 downto 0);
        branch     : out std_logic
        );        
end EX;

architecture comb of EX is
component RISCV_ALU is
  Port (A        : in  std_logic_vector(31 downto 0);  
        B        : in  std_logic_vector(31 downto 0);  
        selALUOp : in  std_logic_vector( 3 downto 0);  
		ALUOut   : out std_logic_vector(31 downto 0);  
        branch   : out std_logic 
        );        
end component;

signal A 	  	   : std_logic_vector(31 downto 0);  
signal B 	  	   : std_logic_vector(31 downto 0);  
signal brBaseAdd   : std_logic_vector(31 downto 0);   

begin

selA_i: process (auipc, rs1D, PC) 					
begin
  A <= rs1D; -- default 
  if auipc = '1' then 
     A  <= PC;
  end if;
end process;


selB_i: process(selALUBSrc, rs2D, extImm) 			
begin
   B <= extImm; -- default 
   if selALUBSrc = '1' then
      B <= rs2D;  
   end if;
end process;

ALU_i: RISCV_ALU Port map 							
         (A        => A, 
          B        => B, 
          selALUOp => selALUOp, 
		  ALUOut   => ALUOut,   
		  branch   => branch
        );        

DToM_i: process(selDToM, rs2D) 
begin
	DToM <= (others => '0'); -- default
	case selDToM is
		when "00" => DToM              <= rs2D; 		     -- SW store word     instruction
		when "01" => DToM(15 downto 0) <= rs2D(15 downto 0); -- SH store halfword instruction
		when "10" => DToM( 7 downto 0) <= rs2D( 7 downto 0); -- SB store byte     instruction
		when others => null; 
	end case;
end process;

brBaseAdd_i: process(jalr, PC, rs1D) 	
begin
   brBaseAdd <= PC; -- default 
   if jalr = '1' then
      brBaseAdd <= rs1D;  
   end if;
end process;

genbrAdd_i: brAdd <= std_logic_vector( signed(brBaseAdd) + signed(extImm) ); 

end comb;