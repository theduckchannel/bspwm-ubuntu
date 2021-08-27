#!/usr/bin/python3
import os
import sys
import configparser
import time
import subprocess as sp

cp = configparser.ConfigParser(allow_no_value=True)
cp.read('packages.ini')
username = sp.getoutput('whoami')


def cprint( fmt, fg=None, bg=None, style=None ):
    """
    Colour-printer.

        cprint( 'Hello!' )                                  # normal
        cprint( 'Hello!', fg='g' )                          # green
        cprint( 'Hello!', fg='r', bg='w', style='bx' )      # bold red blinking on white

    List of colours (for fg and bg):
        k   black
        r   red
        g   green
        y   yellow
        b   blue
        m   magenta
        c   cyan
        w   white

    List of styles:
        b   bold
        i   italic
        u   underline
        s   strikethrough
        x   blinking
        r   reverse
        y   fast blinking
        f   faint
        h   hide
    """

    COLCODE = {
        'k': 0, # black
        'r': 1, # red
        'g': 2, # green
        'y': 3, # yellow
        'b': 4, # blue
        'm': 5, # magenta
        'c': 6, # cyan
        'w': 7  # white
    }

    FMTCODE = {
        'b': 1, # bold
        'f': 2, # faint
        'i': 3, # italic
        'u': 4, # underline
        'x': 5, # blinking
        'y': 6, # fast blinking
        'r': 7, # reverse
        'h': 8, # hide
        's': 9, # strikethrough
    }

    # properties
    props = []
    if isinstance(style,str):
        props = [ FMTCODE[s] for s in style ]
    if isinstance(fg,str):
        props.append( 30 + COLCODE[fg] )
    if isinstance(bg,str):
        props.append( 40 + COLCODE[bg] )

    # display
    props = ';'.join([ str(x) for x in props ])
    if props:
        print( '\x1b[%sm%s\x1b[0m' % (props, fmt) )
    else:
        print( fmt )



def cmd(parameter):
    os.system(parameter)
    

def pause(param=3):
    time.sleep(param)


def showWelcomeScreen():
    cmd('clear')
    cprint('===========================================================', fg='y', style='b')
    cprint(':: The Duck Channel´s Ubuntu 21.04 bspwm Style ::', fg='g', style='b')
    cprint('https://github.com/theduckchannel/bspwm-ubuntu', fg='c', style='b')
    cprint('===========================================================', fg='y', style='b')
    pause()

 
def installRegularPackages():
    cprint('\r\n:: Installing Regular packages...', fg='y', style='b')
    pause(2)
    regPkgs = ''
    for pkg in cp['Regular']:
        regPkgs = regPkgs + pkg + ' '

    print(regPkgs)
    os.system(f'sudo apt install --assume-yes {regPkgs}')
    pause()

def installNonRegularPackages():
    cprint('\r\n:: Install Non Regular Packages...', fg='y', style='b')
    pause(2)
    cmd('fc-cache -fv')
    cprint('\r\n:: Install i3lock-color...', fg='g', style='b')
    cmd('git clone https://github.com/Raymo111/i3lock-color.git')
    cmd('cd i3lock-color')
    os.chdir('i3lock-color/')
    cmd('sudo ./install-i3lock-color.sh')
    os.chdir('../')
    cmd('sudo rm -rf i3lock-color')

    pause()


def installDotFiles():
    # if ~/.config not exists, so create
    cprint('\r\n:: Installing dotfiles...', fg='y', style='b')
    if(not os.path.isdir(f'/home/{username}/.config')):
        os.mkdir(f'/home/{username}/.config')
    #yes | cp fonts/* ~/.local/share/fonts
    os.system(f'cp -rf {os.getcwd()}/dotfiles/.config/* /home/{username}/.config')
    os.system(f'cp -rf {os.getcwd()}/dotfiles/.Xre* /home/{username}/')
    os.system(f'cp -rf {os.getcwd()}/dotfiles/.xs* /home/{username}/')
    os.system(f'cp -rf {os.getcwd()}/dotfiles/.fe* /home/{username}/')
    os.system(f'cp -rf {os.getcwd()}/dotfiles/.vimrc /home/{username}/')
    pause()


def updateAndUpgrade():
    cprint('\r\n:: Update and Upgrading your system...', fg='y', style='b')
    pause(2)
    os.system('sudo apt --assume-yes update')
    os.system('sudo apt --assume-yes upgrade')
    pause()

def showFinalMessage():
    cprint('\r\n:: Everything ok...', fg='y', style='b')
    input('Press any key to REBOOT!')
    os.system('reboot')


def polyBarConfig():
    cprint('\r\n:: Polybar Config...', fg='y', style='b')
    os.system('./polybar-config.sh')
    

def installOhMyBash():
    cprint('\r\n:: Installl oh-my-bash...', fg='y', style='b')
    pause(2)
    cmd('cp -rf dotfiles/.oh-my-bash/ ~/')
    cmd('cp -rf dotfiles/.bashrc ~/')
    pause()


def installNerdFont():
    cprint('\r\n:: Installl Nerd Font...', fg='y', style='b')
    pause(2)
    cmd('mkdir -p ~/.local/share/fonts')
    cmd('wget "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip"')
    cmd('unzip -o -d ~/.local/share/fonts/ FiraCode.zip')
    cmd('fc-cache -fv')
    cmd('rm -rf FiraCode.zip')
    pause()


def main():
    showWelcomeScreen()
    updateAndUpgrade()
    installRegularPackages()
    installNonRegularPackages()
    installDotFiles()
    polyBarConfig()
    installOhMyBash()
    installNerdFont()
    showFinalMessage()
    

if __name__ == "__main__":
    main()
