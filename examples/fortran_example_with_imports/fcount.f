* add a big number of times
	open(file="fcount.in.txt", unit=10, status="old")

	read(10,*) inumber
	write(*,*) inumber
	close(10)

	j=0
	do i=1,inumber
	  j=j+1
	end do
	open(file="fcount.out.txt", unit=12)
	write(12,*) "J is now", j
	  
	write(*,*) j
	end


