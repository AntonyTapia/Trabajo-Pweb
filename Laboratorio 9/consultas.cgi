#!"C:/xampp/perl/bin/perl.exe"
use CGI::Carp 'fatalsToBrowser';
use Encode qw(decode);
use CGI;
my $cgi = CGI->new;
my $nombre = decode('UTF-8', $cgi->param('nombreU'));
my $periodo = $cgi->param('periodoL');
my $departamento = decode('UTF-8', $cgi->param('departamentoL'));
my $denominacion = decode('UTF-8', $cgi->param('denominacionP'));
my $regresar = $cgi->param('regresar');

if ($regresar){
    print $cgi->redirect('http://localhost/Consultas.html');
} else {
    my $archivo;
    my $aja;
    open($archivo, "Programas_de_Universidades.csv");
    my @archivo = <$archivo>;
    close($archivo);

    open(my $resultadosHTML, "../htdocs/Resultados.html");
    my @resultadosHTML = <$resultadosHTML>;
    close $resultadosHTML;

    my $tablaInicio;
    my $tablaFin;
    for (my $i = 0; $i < @resultadosHTML; $i++){
        if ($resultadosHTML[$i] =~ /<table/) {
            $tablaInicio = $i+1;
        } elsif ($resultadosHTML[$i] =~ /<\/table>/) {
            $tablaFin= $i;
        }
    }
    splice(@resultadosHTML, $tablaInicio, $tablaFin-$tablaInicio);

    for (my $i = 0; $i < @resultadosHTML; $i++){
        if ($resultadosHTML[$i] =~ /<table/) {
            my $control = 0;
            for (my $j = 0; $j < @archivo; $j++){
                my @campos = $archivo[$j] =~ /([^|]+)/g;
                if ($j == 0) {
                    my $tipo = "th";
                    splice(@resultadosHTML, $i+1, 0, registros(@campos, $tipo));
                    $i++;
                    $control = @campos;
                } elsif ($nombre && $periodo && $departamento && $denominacion &&
                    $campos[1] eq $nombre && $campos[4] eq $periodo && $campos[10] eq $departamento && $campos[16] eq $denominacion) {
                    my $tipo = "td";
                    splice(@resultadosHTML, $i+1, 0, registros(@campos, $tipo));
                    $i++;
                    $control = 0;
                }
            }
            if ($control){
                splice(@resultadosHTML, $i+1, 0, "<td colspan=\"$control\">No se encontraron resultados</td>\n");
            }
        }
    }

    sub registros {
        my $tipo = $_[@_-1];
        my $registro = "<tr>\n";
        for (my $i = 0; $i < @_-1; $i++){
            $_[$i] =~ s/_/ /g;
            $registro .= "<$tipo>$_[$i]</$tipo>\n";
        }
        $registro .= "</tr>\n";
        return $registro;
    }


    open my $resultadosHTML, '>:utf8', '../htdocs/Resultados.html';
    print $resultadosHTML @resultadosHTML;
    close $resultadosHTML;

    print $cgi->redirect('http://localhost/Resultados.html');
}