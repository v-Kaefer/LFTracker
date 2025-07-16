# Maintainer: Kaleb
pkgname=lftracker
pkgver=0.1.0
pkgrel=1
pkgdesc="A Tracker for used and unused packages in linux."
arch=('any')
url="https://github.com/v-Kaefer/LFTracker"
license=('MIT')
depends=('python' 'python-pyqt5' 'pacman-contrib' 'expac')
source=(
  "cleanup/main.py"
  "cleanup/ui.py"
  "lftracker.desktop"
)
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
    # Exec in /usr/bin
    install -Dm755 "$srcdir/main.py" "$pkgdir/usr/bin/lftracker"

    # UI in /usr/share/lftracker
    install -Dm644 "$srcdir/ui.py" "$pkgdir/usr/share/lftracker/ui.py"

    # Binary path
    sed -i "1a import sys\nsys.path.insert(0, \"/usr/share/lftracker\")" "$pkgdir/usr/bin/lftracker"

    # Icon (optional)
    #install -Dm644 "$srcdir/lftracker.desktop" "$pkgdir/usr/share/applications/lftracker.desktop"
}
