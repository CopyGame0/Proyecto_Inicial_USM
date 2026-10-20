#pregunta al formulario ¿que preferencias tiene el usuario?

from dataclasses import dataclass, field

@dataclass(frozen=True)
class NutrutionPreferences:
    dita: str | None = None #opcional (aunque no deveria, es toda la gracia XD) Talvez sea editado despues
    #separados por comas
    intolerancias: tuple[str, ...] = ()
    incluye_Ingredients : tuple[str, ...] = () #Un tuple de ingedientes :v 
    excluye_ingredients: tuple[str, ...] = ()
    sort: str = "random"
    
    minCalories : int | None = None #Calorias minimas, opcional
    maxCalories : int | None = None #Calorias maximas, opcional
    minProteina : int | None = None #Proteinas Minimas,opcional
    maxProteina : int | None = None #Proteinas Maximas,opcional
    minCarbs    : int | None = None #opcional
    maxCarbs    : int | None = None #opcional
    minAzucar   : int | None = None #opcional
    maxAzucar   : int | None = None #opcional
    
    #funcion para convertir los parametros de python a un formato HTTP de la API
    
    def to_api_params(self) -> dict: #referencia a la misma clase y retorna un diccionario.
        parametros = {}
        
        if self.dita:
            parametros["diet"] = self.dita
        if self.sort:
            parametros["sort"] = self.sort
            
        #ingredientes e intolerancias
        if self.intolerancias:
            parametros["intolerances"] = self.intolerancias
        if self.incluye_Ingredients:
            parametros["includeIngredients"] = ",".join(self.incluye_Ingredients)
        if self.excluye_ingredients:
            parametros["excludeIngredients"] = ",".join(self.excluye_ingredients)

            
        # Calorías
        if self.minCalories is not None:
            parametros["minCalories"] = self.minCalories
        if self.maxCalories is not None:
            parametros["maxCalories"] = self.maxCalories 
            
        # Proteínas
        if self.minProteina is not None:
            parametros["minProtein"] = self.minProteina
        if self.maxProteina is not None:
            parametros["maxProtein"] = self.maxProteina
            
        # Carbohidratos
        if self.minCarbs is not None:
            parametros["minCarbs"] = self.minCarbs
        if self.maxCarbs is not None:
            parametros["maxCarbs"] = self.maxCarbs
            
        # Azúcar
        if self.minAzucar is not None:
            parametros["minSugar"] = self.minAzucar
        if self.maxAzucar is not None:
            parametros["maxSugar"] = self.maxAzucar
        
            
        return parametros
    
    
    
    