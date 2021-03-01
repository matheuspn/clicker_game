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
            "base_production": 50,
            "rate": 1.15,
        }
    })

    def new_cost(self, cost_base, rate, owned):
        return cost_base * (rate ** owned)
        

    def shop_button1(self):
        # aumentando o número de upgrades
        manager.upgrades["button1"]["owned"] += 1
        # debitando o valor
        manager.gold -= manager.upgrades["button1"]["cost"]
        # aumentando a produção
        manager.upgrades["button1"]["production"] = (
            self.base_buttons["button1"]["base_production"] * manager.upgrades["button1"]["owned"]
            ) *  manager.upgrades["button1"]["multipliers"]
        print(manager.upgrades["button1"]["production"])
        # atribuindo novo valor de compra
        manager.upgrades["button1"]["cost"] += self.new_cost(
            self.base_buttons["button1"]["base_cost"],
            self.base_buttons["button1"]["rate"],
            manager.upgrades["button1"]["owned"] )
        # atualizando valor de compra na tela
        self.ids.b1_cost.text = str(round(manager.upgrades["button1"]["cost"], 2))


class Manager(ScreenManager):
    
    upgrades = DictProperty({
        "button1": {
            "cost" : 10,
            "owned" : 0,
            "multipliers": 1,
            "production": 0
        }
    })

    gold = NumericProperty(0.0)
    production = NumericProperty(0.0)
      
    def update(self, dt):
        # testando se é possível comprar o upgrade
        if self.gold < self.upgrades["button1"]["cost"]:
            self.get_screen('shop').ids.b1_cost.disabled = True
        else: self.get_screen('shop').ids.b1_cost.disabled = False

        self.get_screen('home').ids.money.text = f"{self.gold:.1f} gold"
        self.get_screen('shop').ids.money.text = f"{self.gold:.1f} gold"

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