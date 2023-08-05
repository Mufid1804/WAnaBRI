#!/usr/bin/env python3

"""Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.
For internal purpose use only.
"""

from dataclasses import dataclass


@dataclass
class Color:
    """ANSI colors."""
    W: str = '\033[1;97m'
    Y: str = '\033[1;93m'
    G: str = '\033[1;92m'
    R: str = '\033[1;91m'
    B: str = '\033[1;94m'
    C: str = '\033[1;96m'
    E: str = '\033[0m'

    @classmethod
    def disable(cls):
        """Disables all colors."""
        cls.W = ''
        cls.Y = ''
        cls.G = ''
        cls.R = ''
        cls.B = ''
        cls.C = ''
        cls.E = ''

    @classmethod
    def unpack(cls):
        """Unpacks and returns the color values.
        Useful for brevity, e.g.:
        (W,Y,G,R,B,C,E) = Color.unpack()
        """
        return (cls.W, 
                cls.Y,
                cls.G,
                cls.R,
                cls.B,
                cls.C,
                cls.E
                )

def asciiart():
    (W,Y,G,R,B,C,E) = Color.unpack()
    logo = f"""
 
{R} __       __   ______                      {B} _______   _______   ______                         
{R}/  |  _  /  | /      \                     {B}/       \ /       \ /      |{G}                        
{R}$$ | / \ $$ |/$$$$$$  | _______    ______  {B}$$$$$$$  |$$$$$$$  |$$$$$$/ {G}      ______   __    __ 
{R}$$ |/$  \$$ |$$ |__$$ |/       \  /      \ {B}$$ |__$$ |$$ |__$$ |  $$ |  {G}     /      \ /  |  /  |
{R}$$ /$$$  $$ |$$    $$ |$$$$$$$  | $$$$$$  |{B}$$    $$< $$    $$<   $$ |  {G}    /$$$$$$  |$$ |  $$ |
{R}$$ $$/$$ $$ |$$$$$$$$ |$$ |  $$ | /    $$ |{B}$$$$$$$  |$$$$$$$  |  $$ |  {G}    $$ |  $$ |$$ |  $$ |
{R}$$$$/  $$$$ |$$ |  $$ |$$ |  $$ |/$$$$$$$ |{B}$$ |__$$ |$$ |  $$ | _$$ |_ {G} __ $$ |__$$ |$$ \__$$ |
{R}$$$/    $$$ |$$ |  $$ |$$ |  $$ |$$    $$ |{B}$$    $$/ $$ |  $$ |/ $$   |{G}/  |$$    $$/ $$    $$ |
{R}$$/      $$/ $$/   $$/ $$/   $$/  $$$$$$$/ {B}$$$$$$$/  $$/   $$/ $$$$$$/ {G}$$/ $$$$$$$/   $$$$$$$ |
                                                                           {G}$$ |      /  \__$$ |
{W}Develop by Muhammad Mufid                                                  {G}$$ |      $$    $$/ 
{W}Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.                    {G}$$/        $$$$$$/  
    """+E

    return logo

