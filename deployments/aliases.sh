alias k=kubectl
alias cls=clear
alias python=python3
alias py=python3
check_port() {
    sudo ss -lptn "sport = :$1"
}