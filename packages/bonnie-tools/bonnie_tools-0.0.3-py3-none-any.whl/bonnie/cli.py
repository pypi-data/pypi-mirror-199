# coding: utf-8

import click
from bonnie.excel.entry import dispatch


@click.group()
def cli():
    """BonnieTools - Command line tool for Bonnie"""
    pass


@cli.command()
def excel():
    dispatch()
