# Maintainer: Kaleb
pkgname=lftracker
pkgver=0.1.0
pkgrel=1
pkgdesc="A Tracker for used and unused packages in linux."
arch=('any')
url="https://github.com/your-user/arch-cleanup-ui"
license=('MIT')
depends=('python' 'python-pyqt5' 'ncdu' 'audit')
makedepends=('python-setuptools')
source=("cleanup/")
md5sums=('SKIP')

package() {
  install -d "$pkgdir/usr/bin"
  install -m755 cleanup/main.py "$pkgdir/usr/bin/arch-cleanup-ui"
}
