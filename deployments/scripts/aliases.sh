# Usefule aliases to work with the cluster. No input arguments.
# Example usage:
#   ./aliases.sh
alias k=kubectl
alias cls=clear
alias python=python3
alias py=python3
check_port() {
    sudo ss -lptn "sport = :$1"
}