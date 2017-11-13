#!/usr/bin/env python

""" ecies.py
      
    Python implementation of an Elliptic Curve Integrated Encryption Scheme

    Copyright 2017, Zane Witherspoon
"""
from ecc.curves import SECP_256k1
from ecc.curves import SmallWeierstrassCurveFp
from ecc.ecc import string_to_int, int_to_string
import os
import pwd
import click
import pyqrcode
import binascii
from sha3 import sha3_256


def ecies():
    #SECP_256K1 is both the Ethereum and Bitcoin Standard
    curve = SECP_256k1()
    G = curve.generator()
    private = string_to_int( os.urandom(curve.coord_size) )
    public = private * G

    click.echo("private int")
    click.echo(private)
    click.echo("pub x and y")
    click.echo(public.x)
    click.echo(public.y)
    click.echo("keccak hash of pub.x")
    keccak = sha3_256(int_to_string(public.x))
    click.echo(keccak.hexdigest())


    priv_b58 = b58encode( int_to_string(private) )
    pub_b58 = b58encode( int_to_string(public.x) )

    
    click.echo( 'private key: {}'.format(priv_b58) )
    priv_qr_string = 'bc:' + priv_b58
    qr = pyqrcode.create( priv_qr_string )
    text_qr = qr.terminal()
    #click.echo(text_qr)

    
    click.echo( 'public key: {}'.format(pub_b58) )
    pub_qr_string = 'bc:' + pub_b58
    qr = pyqrcode.create( pub_qr_string )
    text_qr = qr.terminal()
    #click.echo(text_qr)

    click.echo( 'Eth Address: 0x' + keccak.hexdigest()[-40:] )
    #add_qr_string = 'bc:' + pub_b58
    #qr = pyqrcode.create( pub_qr_string )
    #text_qr = qr.terminal()
    #click.echo(text_qr)



### BEGIN: Copied from https://bitcointalk.org/index.php?topic=1026.0 (public domain)
__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)
def b58encode(v):
  """ encode v, which is a string of bytes, to base58.
  """

  long_value = 0
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)

  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result

  # Bitcoin does a little leading-zero-compression:
  # leading 0-bytes in the input become leading-1s
  nPad = 0
  for c in v:
    if c == '\0': nPad += 1
    else: break

  return (__b58chars[0]*nPad) + result


# ---- Command line interface -----------------------------
class Options(object):
    def __init__(self):
        self.verbose = False
pass_options = click.make_pass_decorator(Options, ensure=True)

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--cipher_suite', '-c', 'cipher_suite_name',
              help="Cipher suite to use for the command.")
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Verbose output')
@click.option('--wallet', '-w', 'wallet_path', type=click.Path(exists=True),
               default=None,
               help="Path to wallet, default is ~/.tip/wallet")
@pass_options
def cli(options, cipher_suite_name, verbose, wallet_path): # entry point for cli
    """ ECC Toy.
    """
    options.cipher_suite_name = cipher_suite_name
    options.verbose = verbose
    # if path not specified, open ~/.tip/wallet
    if not wallet_path:
        user_dir = pwd.getpwuid(os.geteuid()).pw_dir
        wallet_path = user_dir + '/.tip/wallet'
    options.wallet_path = wallet_path

# QR code output of Persona
# ---- tip [options] qr [-p][-t][--qz NUM] -----------------------------
@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--txt', '-t', 'out_format', flag_value='txt', default=True,
              help='Output a text version of the QR code.')
@click.option('--png', '-p', 'out_format', flag_value='png',
              help='Output a png image of the QR code.')
@click.option('--qz', 'quiet_zone', default=1,
              help='Set size of quiet zone around QR code.')
@pass_options
def qr(options, out_format, quiet_zone):
    """ Output as QR code.
    """
    wallet=Wallet(options.wallet_path)

    qr_string = 't:' + '123123123'
    qr = pyqrcode.create( qr_string )
    text_qr = qr.terminal(quiet_zone=quiet_zone)
    click.echo(text_qr)


# ---- tip [options] new [-p <name] ------------------------------------
@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--name', '-n', 'persona_name', default=None,
              help='The local name of the persona.')
@pass_options
def new(options, persona_name):
    """  """
    pass



@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@pass_options
def toy(options):
    ecc_toy()

@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@pass_options
def toy2(options):
    ecc_toy2()

if __name__ == '__main__':
    cli()
