-- Copyright (C) 2023  Intel Corporation. All rights reserved.
-- Your use of Intel Corporation's design tools, logic functions 
-- and other software and tools, and any partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Intel Program License 
-- Subscription Agreement, the Intel Quartus Prime License Agreement,
-- the Intel FPGA IP License Agreement, or other applicable license
-- agreement, including, without limitation, that your use is for
-- the sole purpose of programming logic devices manufactured by
-- Intel and sold by Intel or its authorized distributors.  Please
-- refer to the applicable agreement for further details, at
-- https://fpgasoftware.intel.com/eula.

-- VENDOR "Altera"
-- PROGRAM "Quartus Prime"
-- VERSION "Version 22.1std.1 Build 917 02/14/2023 SC Lite Edition"

-- DATE "03/30/2023 21:42:51"

-- 
-- Device: Altera 5CSEBA6U23I7 Package UFBGA672
-- 

-- 
-- This VHDL file should be used for Questa Intel FPGA (VHDL) only
-- 

LIBRARY ALTERA_LNSIM;
LIBRARY CYCLONEV;
LIBRARY IEEE;
USE ALTERA_LNSIM.ALTERA_LNSIM_COMPONENTS.ALL;
USE CYCLONEV.CYCLONEV_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	mux21_1 IS
    PORT (
	sel : IN std_logic;
	muxIn1 : IN std_logic;
	muxIn0 : IN std_logic;
	muxOut : BUFFER std_logic
	);
END mux21_1;

-- Design Ports Information
-- muxOut	=>  Location: PIN_AA26,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- sel	=>  Location: PIN_AB26,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- muxIn1	=>  Location: PIN_W21,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- muxIn0	=>  Location: PIN_W20,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF mux21_1 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_sel : std_logic;
SIGNAL ww_muxIn1 : std_logic;
SIGNAL ww_muxIn0 : std_logic;
SIGNAL ww_muxOut : std_logic;
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \muxIn0~input_o\ : std_logic;
SIGNAL \muxIn1~input_o\ : std_logic;
SIGNAL \sel~input_o\ : std_logic;
SIGNAL \muxOut~0_combout\ : std_logic;
SIGNAL \ALT_INV_sel~input_o\ : std_logic;
SIGNAL \ALT_INV_muxIn0~input_o\ : std_logic;
SIGNAL \ALT_INV_muxIn1~input_o\ : std_logic;

BEGIN

ww_sel <= sel;
ww_muxIn1 <= muxIn1;
ww_muxIn0 <= muxIn0;
muxOut <= ww_muxOut;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
\ALT_INV_sel~input_o\ <= NOT \sel~input_o\;
\ALT_INV_muxIn0~input_o\ <= NOT \muxIn0~input_o\;
\ALT_INV_muxIn1~input_o\ <= NOT \muxIn1~input_o\;

-- Location: IOOBUF_X89_Y23_N56
\muxOut~output\ : cyclonev_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false",
	shift_series_termination_control => "false")
-- pragma translate_on
PORT MAP (
	i => \muxOut~0_combout\,
	devoe => ww_devoe,
	o => ww_muxOut);

-- Location: IOIBUF_X89_Y23_N21
\muxIn0~input\ : cyclonev_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_muxIn0,
	o => \muxIn0~input_o\);

-- Location: IOIBUF_X89_Y23_N4
\muxIn1~input\ : cyclonev_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_muxIn1,
	o => \muxIn1~input_o\);

-- Location: IOIBUF_X89_Y23_N38
\sel~input\ : cyclonev_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_sel,
	o => \sel~input_o\);

-- Location: LABCELL_X88_Y23_N0
\muxOut~0\ : cyclonev_lcell_comb
-- Equation(s):
-- \muxOut~0_combout\ = ( \sel~input_o\ & ( \muxIn1~input_o\ ) ) # ( !\sel~input_o\ & ( \muxIn0~input_o\ ) )

-- pragma translate_off
GENERIC MAP (
	extended_lut => "off",
	lut_mask => "0101010101010101010101010101010100001111000011110000111100001111",
	shared_arith => "off")
-- pragma translate_on
PORT MAP (
	dataa => \ALT_INV_muxIn0~input_o\,
	datac => \ALT_INV_muxIn1~input_o\,
	dataf => \ALT_INV_sel~input_o\,
	combout => \muxOut~0_combout\);

-- Location: LABCELL_X85_Y28_N3
\~QUARTUS_CREATED_GND~I\ : cyclonev_lcell_comb
-- Equation(s):

-- pragma translate_off
GENERIC MAP (
	extended_lut => "off",
	lut_mask => "0000000000000000000000000000000000000000000000000000000000000000",
	shared_arith => "off")
-- pragma translate_on
;
END structure;


