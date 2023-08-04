import collections
def exgcd(a, b):
	if b == 0:
	    return 1, 0, a
	x, y, gcd = exgcd(b, a % b)
	return y, x - a // b * y, gcd

def get_inv(a, b):
	x, y, gcd = exgcd(a, b)
	if gcd == 1:
		return (x % b + b) % b
	else:
		raise Exception("不存在逆元")


EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

curve = EllipticCurve(
    name='Secp256k1',
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)

def on_curve(point: tuple) -> bool:
    if point is None:
        return True
    x, y = point
    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def negative(point: tuple) -> tuple or None:
    assert on_curve(point)
    if point is None:
        return None
    x, y = point
    result = (x, -y % curve.p)
    assert on_curve(result)
    return result

def add(p: tuple, q: tuple) -> tuple or None:
    assert on_curve(p)
    assert on_curve(q)
    if p is None:
        return q
    if q is None:
        return p

    if p == negative(q):
        return None

    x1, y1 = p
    x2, y2 = q
    if p == q:
        m = (3 * x1 * x1 + curve.a) * get_inv(2 * y1, curve.p)
    else:
        m = (y1 - y2) * get_inv(x1 - x2, curve.p)
    x = m * m - x1 - x2
    y = y1 + m * (x - x1)
    result = (x % curve.p, -y % curve.p)
    assert on_curve(result)
    return result


def mul(k: int, point: tuple) -> tuple or None:
    assert on_curve(point)
    if k % curve.n == 0 or point is None:
        return None
    if k < 0:
        return mul(-k, negative(point))
    result = None
    while k:
        if k & 1:
            result = add(result, point)
        point = add(point, point)
        k >>= 1
    assert on_curve(result)
    return result


bg= mul(0x2, curve.g)
cg=mul(0xa, curve.g)
dg=add(bg,cg)
r=dg[0]%(curve.n)
print('r=',hex(r))
ee=r*2*get_inv(5,curve.n)
e=ee%curve.n
print('e=',hex(e))
ss=r*get_inv(5,curve.n)
s=ss%curve.n
print('s=', hex(s))