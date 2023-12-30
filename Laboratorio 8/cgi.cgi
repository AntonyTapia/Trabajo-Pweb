#!"C:\xampp\perl\bin\perl.exe"
use strict;
use CGI;
use warnings;

print "Content-type: text/html\n\n";
print <<HTML;
<!DOCTYPE html>
<html>
  <head> 
    <meta charset="utf-8"> 
    <title>Calcular </title>
    <style>
        body{
            text-align: center;
        }
        .sol{
            font-size: 3rem;
            background-color: rgb(240, 14, 86);
        }
        input[type="submit"]{
            display: block;
            margin: auto;
            margin-top: 5rem;
            font-family: 'Vina Sans', sans-serif;
            font-size: 30px;
            padding: 10px;
            background-color: palevioletred;
        }
    </style>
  </head>
<body>
    <div class = "sol">
HTML
my $q = CGI->new;
my $expresion = $q->param('expresion');
print "La expresión es $expresion <br>\n";;
#Es expresion matematica? 
#^: Representa el inicio de la cadena.
#[0-9: Coincide con cualquier dígito del 0 al 9.
#+\-*\/: Coincide con los caracteres +, *, - o /.
#+: Indica que la clase de caracteres anterior (los dígitos y los signos) debe aparecer al menos una vez.
#$: Representa el final de la cadena.
my $line = $expresion;
if($line =~ /^[0-9+\-*\/(\)]+$/){
    print "ES EXPRESION MATEMATICA <br>\n";
    if(comprobarParentesis($line)){
        my $resultado = evaluar_subexpresiones($expresion);
        print "$resultado <br>";
    }else{
        print "ERROR EN PARENTESIS <br>\n";

    }
}else{
    print "NO ES EXPRESION MATEMATICA \n";
}
#VERIFICAMOS LOS PARENTESIS
print <<HTML;
    </div>
    <form action="../index.html">
        <input type="submit" value="Regresar">
    </form>
</body>
</html>
HTML
#Logica:
#Primero reconocer si es una expresion matematica -> solo debe haber numeros y signos de operacion (+-*/)
#Luego -> si hay algun parentesis, hacer un codigo para validar si estos son correctos.
#Por ultimo, operar los elementos con expresiones regulares
sub comprobarParentesis {
    my ($cadena) = @_;
    my $contador = 0;
    my $longitud = length($cadena);
    for my $i (0 .. $longitud - 1) {
        my $caracter = substr($cadena, $i, 1);
        if ($caracter eq '(') {
            $contador++;
        } elsif ($caracter eq ')') {
            $contador--;
        }
    if ($contador < 0) {
        return 0;
    }
}
    if ($contador == 0) {
        return 1;
    } else {
        return 0;
    }
}
sub evaluar_subexpresiones {
    my ($expresion) = @_;
    # Evaluar subexpresiones entre paréntesis
    # Aplica un enfoque recursivo:
    while ($expresion =~ /\(([^()]+)\)/) { #Evalua si hay expresiones entre parentesis
        my $subexpresion = $1; #Captura la expresion si se encuentra
        my $resultado_sub = evaluar_subexpresiones($subexpresion); #Aplica recursivamente el algoritmo, buscando mas expresiones entre parentesis con mayor prioridad
        return "Error" unless defined $resultado_sub; #Retorna un error si $resultado_sub es indefinido
        $expresion =~ s/\Q($subexpresion)\E/$resultado_sub/; #Expresion regular para reemplazar $resultado_sub en $subexpresion
    }
    # Evaluar multiplicación y división
    while ($expresion =~ /(\d+)([\*\/])(\d+)/) { #Busca cualquier expresion de la forma a*b o a/b
        my ($num1, $op, $num2) = ($1, $2, $3); #Se capturan los caracteres
        my $resultado_op = $op eq '*' ? $num1 * $num2 : $num1 / $num2;
        $expresion =~ s/\Q$num1$op$num2\E/$resultado_op/;
    }
    # Evaluar suma y resta
    while ($expresion =~ /(\d+)([\+\-])(\d+)/) {
        my ($num1, $op, $num2) = ($1, $2, $3);
        my $resultado_op = $op eq '+' ? $num1 + $num2 : $num1 - $num2;
        $expresion =~ s/\Q$num1$op$num2\E/$resultado_op/;
    }
    return $expresion;
}
#Casos de prueba
#1+3+4+5
#1+3+4+5*7
#1+3+(5+6)*9
#(1+(1+(4+9)*9))/2