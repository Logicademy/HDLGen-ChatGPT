-- Company: National University of Ireland Galway
-- Engineer: Fearghal Morgan, Arthur Beretta (AB), Joseph Clancy (JC)
-- Created June 2018
--
-- Module Name: RISCV_WB
-- Description: Writeback component
--
-- Includes 
--  1. 3-to-1 WBDat selection multiplexer
--  2. selLdSlice for memory read slice selection

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity WB is
   Port (selWBD   : in  std_logic_vector( 1 downto 0);
		 ALUOut   : in  std_logic_vector(31 downto 0);
		 DFrM     : in  std_logic_vector(31 downto 0);
         selDFrM  : in  std_logic_vector(2 downto 0);
		 PCPlus4  : in  std_logic_vector(31 downto 0);
         WBDat    : out std_logic_vector(31 downto 0)
         );
end WB;

architecture combinational of WB is
signal MToWB  : std_logic_vector(31 downto 0); 

begin

selLdSlice_i: process(selDFrM, DFrM)  
begin
    -- selLdSlice component output signal, MToWB selected as sign-extended 32-bit data slice of DFrM
	MToWB <= (others => '0'); -- default
	case selDFrM is                                                                                  -- load instruction
		when "000" => MToWB               <= DFrM;														     -- lw			                                                
		when "001" => MToWB(31 downto 16) <= (others => DFrM(15));  MToWB(15 downto 0) <= DFrM(15 downto 0); -- lh
		when "010" => MToWB(31 downto  8) <= (others => DFrM( 7));  MToWB( 7 downto 0) <= DFrM( 7 downto 0); -- lb
		when "011" => MToWB(31 downto 16) <= (others => '0');       MToWB(15 downto 0) <= DFrM(15 downto 0); -- lhu
		when "100" => MToWB(31 downto  8) <= (others => '0');       MToWB( 7 downto 0) <= DFrM( 7 downto 0); -- lbu
		when others => null; -- MToWB = 0 (default value) 
	end case;
end process;

WBDat_i: process(selWBD, ALUOut, MToWB, PCPlus4)
begin
    WBDat <= (others => '0'); -- default
    case selWBD is
		when "00"      => WBDat <= ALUOut; 
        when "01" 	   => WBDat <= MToWB;
        when "10" 	   => WBDat <= PCPlus4;
        when others => null; -- WBDat = 0 (default value)
    end case;
end process;

end combinational;