#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by weizhenjin on 17-2-14

import click


@click.command()
@click.option('-m', '--message', multiple=True)
def main(message):
    click.echo('\n'.join(message))


if __name__ == '__main__':
    main()
