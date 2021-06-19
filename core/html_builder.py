class HtmlTag:
    def __init__(self, tag : str, attributes : dict = {}, content = ''):
        self.tag : str = tag
        self.attributes : dict = attributes
        self.content = str(content)
    
    def __str__(self):
        attributes_str = " " if len(self.attributes) else ""
        attributes_str +=' '.join([f'{key}="{value}"' for key, value in self.attributes.items()]) 
        return f'<{self.tag + attributes_str}>{self.content}</{self.tag}>'