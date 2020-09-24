#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:45:21 2020

@author: theodorepender
"""
demWinPct = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 180px;
                        background-color: transparent;
                        color: rgb(63, 82, 185);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}%</p>
        </body>
    </html>


"""

repWinPct = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 180px;
                        background-color: transparent;
                        color: rgb(222, 57, 71);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}%</p>
        </body>
    </html>


"""