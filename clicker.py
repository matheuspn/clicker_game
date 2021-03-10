from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, DictProperty
from kivy.clock import Clock


class Home(Screen):
    
    def gold_button(self):
        manager.gold += 1

    
class Shop(Screen):

    base_buttons = DictProperty({
        "button1" : {
            "base_cost": 10,
            "base_production": 0.1,
            "rate": 1.07,
        },
        "button2": {
            "base_cost": 50,
            "base_production": 10,
            "rate": 1.15,
        }
    })

    def new_cost(self, cost_base, rate, owned):
        """
        Define new cost to the buttons
        """
        return cost_base * (rate ** owned)  

    def shop_button(self, n):
        """
        Operation for all upgrade buttons
        """
        # aumentando o número de upgrades
        manager.upgrades[f"button{n}"]["owned"] += 1
        # debitando o valor
        manager.gold -= manager.upgrades[f"button{n}"]["cost"]
        # aumentando a produção
        manager.upgrades[f"button{n}"]["production"] = (
            self.base_buttons[f"button{n}"]["base_production"] * manager.upgrades[f"button{n}"]["owned"]
            ) *  manager.upgrades[f"button{n}"]["multipliers"]
        #print(manager.upgrades[f"button{n}"]["production"])
        # atribuindo novo valor de compra
        manager.upgrades[f"button{n}"]["cost"] += self.new_cost(
            self.base_buttons[f"button{n}"]["base_cost"],
            self.base_buttons[f"button{n}"]["rate"],
            manager.upgrades[f"button{n}"]["owned"] )


class Manager(ScreenManager):
    
    upgrades = DictProperty({
        "button1": {
            "cost" : 10,
            "owned" : 0,
            "multipliers": 1,
            "production": 0
        },
        "button2": {
            "cost" : 50,
            "owned" : 0,
            "multipliers": 1,
            "production": 0
        }
    })

    gold = NumericProperty(0.0)
    production = NumericProperty(0.0)
      
    def update(self, dt):
        shop = self.get_screen('shop')
        home = self.get_screen('home')
        # testando se é possível comprar o upgrade
        # button1
        if self.gold < self.upgrades["button1"]["cost"]:
            shop.ids.b1_cost.disabled = True
        else: shop.ids.b1_cost.disabled = False
        # button2
        if self.gold < self.upgrades["button2"]["cost"]:
            shop.ids.b2_cost.disabled = True
        else: shop.ids.b2_cost.disabled = False

        # atualizando valores de compra na tela
        shop.ids.b1_cost.text = str(round(manager.upgrades["button1"]["cost"], 2))
        shop.ids.b2_cost.text = str(round(manager.upgrades["button2"]["cost"], 2))

        home.ids.money.text = f"{self.gold:.1f} gold"
        shop.ids.money.text = f"{self.gold:.1f} gold"

    def gold_produce(self, dt):
        aux = 0
        for x, y in self.upgrades.items():
            for z, a in y.items():
                if z == "production":
                    aux += a
        self.production = aux
        self.gold += self.production
  

manager = Manager()

class ClickerApp(App):

    def build(self):
        
        manager.add_widget(Home(name= "home"))
        manager.add_widget(Shop(name= "shop"))
        Clock.schedule_interval(manager.update, 1.0 / 30.0)
        Clock.schedule_interval(manager.gold_produce, 1.0)
        return manager

if __name__ == "__main__":
    ClickerApp().run()