-- Company: National University of Ireland Galway
-- Engineer: Fearghal Morgan
-- 
-- Module Name: RB Register Bank  
-- 32 x 32-bit register array x0-x31
-- Description: Register Bank Module for the RISC-V Processor
-- Synchronous write
-- Combinational read 

-- Signal dictionary
--  clk               system clock strobe. low-to-high active edge
--  rst               asynchronous system reset, asserted high
--  ce         		  chip enable
--  rs1(4:0) 	      source address 1 
--  rs2(4:0) 	      source address 2 
--  RWr 	          assertion enables synchronous write of WBDat to RB(rd) 
--  WBDat             writeback data 
--  rd(4:0) 	      destination register address 
--  rs1D(31:0) 	      source address 1 data = RB(rs1), combinational read 
--  rs2D(31:0) 	      source address 2 data = RB(rs2), combinational read 
--  XX_RBArray 		  32 x 32-bit register array, x0-x31 
--                    used in ctrlAndDebug to check for RB breakEvent

--	host memory interface
--     add   	 : 32-bit host address 
--     wr        : assert (h) to write to memory mapped location 
--     dIn 		 : 32-bit data in
--     rd1       : assert (h) to read from memory mapped location. Also use signal rd in this component 
--     dOut	     : 32-bit data out

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.ALL;

entity RB is
  Port (clk      : in  std_logic;
        rst      : in  std_logic;
        ce       : in  std_logic;
        rs1 	 : in  std_logic_vector( 4 downto 0);
        rs2 	 : in  std_logic_vector( 4 downto 0);
		RWr      : in  std_logic;
        WBDat  	 : in  std_logic_vector(31 downto 0);
        rd  	 : in  std_logic_vector( 4 downto 0);
        rs1D     : out std_logic_vector(31 downto 0);
        rs2D     : out std_logic_vector(31 downto 0);

	    XX_RBArray : out RISCV_regType;

	 	-- host-memory interface signals 
        XX_add      : in  std_logic_vector(31 downto 0);
	    XX_wr       : in  std_logic;          
        XX_dIn      : in  std_logic_vector(31 downto 0);
	    XX_rd1      : in  std_logic;          
        XX_dOut     : out std_logic_vector(31 downto 0)
		);
end RB;

architecture RTL of RB is 
signal XX_CS : RISCV_regType;
signal XX_NS : RISCV_regType;
signal XX_memWr 	 : std_logic;                   
signal XX_memRd      : std_logic;                   
signal XX_memRdPulse : std_logic;                  

begin

-- generate local wr signal
asgnMemWr_i: XX_memWr <= '1' when ( XX_wr = '1' and unsigned(XX_add(31 downto 16)) = memMap_RB_32DT16 ) else '0';
		 
NSDecode_i: process(XX_memWr, XX_add, XX_dIn, XX_CS, RWr, rd, WBDat) -- register write next state decode
begin
    XX_NS <= XX_CS;
	if XX_memWr = '1' then 													  -- host write to RB 
	  if XX_add(15 downto 7) = "000000000" and XX_add(1 downto 0) = "00" then -- host RB address is valid, and on 32-bit boundary
	     if XX_add(6 downto 2) /= "00000" then                                -- don't write to register x0 (always 0) 	  
			XX_NS(to_integer(unsigned(XX_add(6 downto 2)))) <= XX_dIn;
		 end if;
   	  end if;
    elsif RWr = '1' and rd /= "00000" then -- RB(0), i.e, x0 always = 0
        XX_NS(to_integer(unsigned(rd))) <= WBDat;
    end if;
end process;
stateReg_i: process(clk, rst) -- State register
begin
    if rst = '1' then
        XX_CS <= (others => (others => '0'));
    elsif rising_edge(clk) then
        if ce = '1' or XX_memWr = '1' then 									  -- register when processor active or host write to RB
            XX_CS <= XX_NS;
        end if;
    end if;
end process;

--asgnRB_i: process (XX_CS)  -- assign RB output signal array
--begin
--  for i in 0 to 31 loop
--    XX_RBArray(i) <= XX_CS(i); 
--  end loop;
--end process;

asgnRB_i: XX_RBArray <= XX_CS; 

-- combination RB outputs
asgn_rs1D_i: rs1D <= XX_CS(to_integer(unsigned(rs1)));
asgn_rs2D_i: rs2D <= XX_CS(to_integer(unsigned(rs2)));


-- host read ==== Start =====
-- generate local rd signal
asgnMemRd_i: XX_memRd <= '1' when ( XX_rd1 = '1' and unsigned(XX_add(31 downto 16)) = memMap_RB_32DT16 ) else '0';
memRdPulse_i: singleShot -- generate rd pulse
Port map (clk      => clk,  
          rst      => '0',  
          XX_sw    => XX_memRd,   	
          XX_aShot => XX_memRdPulse
	     ); 

-- register the addressed location on assertion of host read
dOut_i: process(clk, rst) 
begin
	if rst = '1' then 
		XX_dOut <= (others => '0');
	elsif rising_edge(clk) then
		if XX_memRdPulse = '1' then 
			if XX_add(15 downto 7) = "000000000" and XX_add(1 downto 0) = "00" then 
				XX_dOut <= XX_CS(to_integer(unsigned(XX_add(6 downto 2))));
			end if;			
		end if;
	end if;
end process;
-- host read ==== End =====

-- Assign 12 deep FIFOs, 4-bit wide, x2FIFO for RB(2), x1FIFO for RB(1)
-- for displaying pipeline progression in registers x1 and x2
-- Limited to 4-bit data values.
pipelineFIFOs_i: pipelineFIFOs -- generate 
Port map(clk   => clk,
         rst   => rst,
		 ce    => ce, 
		 RWr   => RWr,
         WBDat => WBDat,
         rd    => rd
         );

end RTL;