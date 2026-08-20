from store.models import Formation, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, formation):
        formation_id = str(formation.id)

        if formation_id in self.cart:
            pass
        else:
            self.cart[formation_id] = float(formation.prix)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def db_add(self, formation_id, price):
        formation_id = str(formation_id)

        if formation_id in self.cart:
            pass
        else:
            self.cart[formation_id] = float(price)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_forms(self):
        formation_ids = self.cart.keys()
        formations = Formation.objects.filter(id__in=[int(id) for id in formation_ids])
        return formations

    def delete(self, formation_id):
        formation_id = str(formation_id)
        if formation_id in self.cart:
            del self.cart[formation_id]
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", "\"")
            current_user.update(old_cart=str(carty))

    def update(self, formation_id, new_price):
        formation_id = str(formation_id)
        if formation_id in self.cart:
            self.cart[formation_id] = float(new_price)
        self.session.modified = True

    def cart_total(self):
        total = sum(float(price) for price in self.cart.values())
        return total